# QuantX AI - Cache Strategy

## Overview

This document defines the caching architecture for QuantX AI using Redis as the primary cache store, including cache patterns, invalidation strategies, TTL policies, and consistency models.

## Cache Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Cache Architecture                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │   Trading    │  │   Strategy   │  │   Market     │  │   User       │ │
│   │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼─────────────────────────────────────────────────────────────┐    │
│   │                    Redis Cluster (6 nodes)                         │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │    │
│   │  │ Market   │  │ Strategy │  │ User     │  │ Session  │         │    │
│   │  │ Cache    │  │ Cache    │  │ Cache    │  │ Cache    │         │    │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Redis Configuration

### Cluster Setup
- **Nodes**: 6 (3 primary, 3 replica)
- **Sharding**: Hash slot partitioning
- **Replication**: Automatic failover
- **Persistence**: RDB + AOF hybrid

### Connection Settings
```python
REDIS_CONFIG = {
    "hosts": ["redis1.quantx.internal:6379", "redis2.quantx.internal:6379"],
    "decode_responses": True,
    "socket_keepalive": True,
    "socket_keepalive_options": {},
    "health_check_interval": 30,
    "retry_on_timeout": True,
    "max_connections": 100,
}
```

## Cache Patterns

### Read-Through Cache
- Check cache first
- Cache miss → DB fetch
- Store in cache
- Return result

```python
async def get_strategy_with_cache(
    strategy_id: StrategyId,
) -> Optional[Strategy]:
    key = f"strategy:{strategy_id}"
    
    # Check cache
    cached = await redis_client.get(key)
    if cached:
        return Strategy(**json.loads(cached))
    
    # DB fetch
    strategy = await strategy_repo.get(strategy_id)
    if strategy:
        await redis_client.setex(
            key, 
            timedelta(minutes=5),
            json.dumps(strategy.model_dump())
        )
    
    return strategy
```

### Write-Through Cache
- Update cache on write
- DB write follows
- Atomic operation when possible

### Cache-Aside (Lazy Loading)
- Application controls cache
- Explicit invalidation
- TTL-based expiration

### Refresh-Ahead Cache
- Proactive cache warming
- Scheduled updates
- Predictive loading

## Cache Key Design

### Key Naming Convention
```
{entity_type}:{entity_id}[:{qualifier}]
```

Examples:
- `strategy:uuid-123`
- `market:BTCUSDT:1h`
- `user:uuid-456:portfolio`
- `session:telegram-123456`

### Key Structure
```python
class CacheKeys:
    @staticmethod
    def strategy(strategy_id: StrategyId) -> str:
        return f"strategy:{strategy_id}"
    
    @staticmethod
    def market_data(symbol: Symbol, timeframe: Timeframe) -> str:
        return f"market:{symbol}:{timeframe}"
    
    @staticmethod
    def user_portfolio(user_id: UserId) -> str:
        return f"user:{user_id}:portfolio"
    
    @staticmethod
    def session(telegram_id: int) -> str:
        return f"session:{telegram_id}"
```

## TTL Policies

### Cache Expiration Matrix
| Cache Type | TTL | Rationale |
|------------|-----|-----------|
| Market Data | 60s | Real-time data |
| Strategy Config | 300s | Infrequent changes |
| User Profile | 3600s | Rare updates |
| Portfolio Value | 30s | Frequent updates |
| Predictions | 300s | Valid for timeframe |
| Session State | 86400s (24h) | User session |
| Rate Limits | 60s | Per-minute limits |

### Slide TTL Pattern
```python
async def get_with_slide_ttl(
    key: str,
    ttl: timedelta,
) -> Optional[Any]:
    cached = await redis_client.get(key)
    if cached:
        # Extend TTL on access
        await redis_client.expire(key, ttl)
    return cached
```

## Cache Invalidation

### Event-Driven Invalidation
```python
EVENT_INVALIDATIONS = {
    "StrategyUpdated": lambda s: f"strategy:{s.id}",
    "PositionOpened": lambda s: f"user:{s.user_id}:portfolio",
    "PositionClosed": lambda s: f"user:{s.user_id}:portfolio",
    "MarketDataUpdated": lambda s: f"market:{s.symbol}:*",
}
```

### Write-Through Invalidation
```python
async def update_strategy(
    strategy: Strategy,
) -> None:
    # Update DB
    await strategy_repo.update(strategy)
    
    # Invalidate cache
    await redis_client.delete(CacheKeys.strategy(strategy.id))
    
    # Warm related caches
    await redis_client.setex(
        CacheKeys.strategy(strategy.id),
        timedelta(minutes=5),
        json.dumps(strategy.model_dump())
    )
```

## Cache Warming

### Startup Warming
```python
async def warm_strategy_cache() -> None:
    """Warm cache with active strategies."""
    active_strategies = await strategy_repo.get_active_strategies()
    pipeline = redis_client.pipeline()
    
    for strategy in active_strategies:
        key = CacheKeys.strategy(strategy.id)
        pipeline.setex(
            key,
            timedelta(minutes=5),
            json.dumps(strategy.model_dump())
        )
    
    await pipeline.execute()
```

### Scheduled Warming
- Every hour for market data
- On service restart
- After deployment
- On failover

## Cache Consistency

### Cache-Aside Consistency
- Last-write-wins
- Event-driven invalidation
- Short TTL for volatile data
- Idempotent writes

### Cache Coherency
- Single source of truth (DB)
- Redis as cache, not primary store
- Read-through for consistency
- Write-through for updates

## Monitoring

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Hit Rate | Cache hits / total | <90% |
| Miss Rate | Cache misses / total | >10% |
| Eviction Rate | Keys evicted | >100/min |
| Memory Usage | Redis memory | >80% |
| Connection Count | Active connections | >80% |

### Redis Metrics
```python
CACHE_METRICS = {
    "cache_hits_total": Counter(
        "quantx_cache_hits_total",
        "Cache hits",
        ["cache_type"]
    ),
    "cache_misses_total": Counter(
        "quantx_cache_misses_total",
        "Cache misses",
        ["cache_type"]
    ),
    "cache_latency_seconds": Histogram(
        "quantx_cache_latency_seconds",
        "Cache operation latency",
        ["operation"]
    ),
}
```

## Related Documents
- [24_MESSAGE_QUEUE.md](24_MESSAGE_QUEUE.md)
- [23_BACKGROUND_WORKERS.md](23_BACKGROUND_WORKERS.md)
- [31_OBSERVABILITY.md](31_OBSERVABILITY.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Infrastructure*