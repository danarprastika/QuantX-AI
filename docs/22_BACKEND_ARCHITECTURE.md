# QuantX AI - Backend Architecture

## Overview

This document describes the backend architecture for QuantX AI services, including API design, service communication, data persistence, and infrastructure integration patterns.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Backend Architecture                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │
│   │   Client     │  │   Load       │  │   API        │                   │
│   │   Request    │  │   Balancer   │  │   Gateway    │                   │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                   │
│          │                 │                 │                           │
│   ┌──────▼──────────────────────────────────────────────────────────┐      │
│   │                    FastAPI Services                              │      │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │      │
│   │  │ Trading  │  │ Strategy   │  │ Market   │  │ User     │       │      │
│   │  │ Service  │  │ Service    │  │ Service  │  │ Service  │       │      │
│   │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │      │
│   │         │             │             │             │           │      │
│   │  ┌──────▼──────────────────────────────────────────────┐      │      │
│   │  │                    Shared Kernel                        │      │      │
│   │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │      │      │
│   │  │  │  Events  │  │ Config   │  │ Logging  │          │      │      │
│   │  │  └──────────┘  └──────────┘  └──────────┘          │      │      │
│   │  └────────────────────────────────────────────────────────┘      │      │
├─────────────────────────────────────────────────────────────────────────────┤
│                        Infrastructure Layer                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   RabbitMQ   │  │    Redis     │  │ PostgreSQL   │  │ TimescaleDB  │ │
│  │   (Events)   │  │   (Cache)    │  │  (Primary)   │  │ (Market Data)│ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   MongoDB    │  │    Vault     │  │   Object     │  │   Kafka      │ │
│  │   (Events)   │  │  (Secrets)   │  │   Storage    │  │   (Future)   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Service Architecture

### Service Bootstrap
```python
# services/trading/infrastructure/container.py
from dependency_injector import containers, providers

class TradingContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # Repositories
    position_repo = providers.Singleton(
        PostgresPositionRepository,
        connection_pool=config.database.pool,
    )
    
    # Services
    exchange_client = providers.Singleton(
        BinanceExchangeAdapter,
        api_key=config.exchange.binance.api_key,
        api_secret=config.exchange.binance.api_secret,
    )
    
    # Use cases
    open_position = providers.Singleton(
        OpenPosition,
        position_repo=position_repo,
        exchange_client=exchange_client,
        event_publisher=config.event_publisher,
    )
```

### FastAPI Application Structure
```python
# services/trading/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    await message_queue.connect()
    yield
    # Shutdown
    await message_queue.disconnect()
    await database.disconnect()

app = FastAPI(
    title="QuantX Trading Service",
    version="1.0.0",
    lifespan=lifespan,
)

# Register routers
app.include_router(
    trading_router,
    prefix="/api/v1/trading",
    tags=["trading"],
)
```

## API Layer Architecture

### Request Flow
```
1. Client Request → API Gateway
2. JWT Validation → Auth Middleware
3. Rate Limiting → Rate Limit Middleware
4. Request Parsing → Pydantic Model
5. Validation → Business Rule Validation
6. Command Creation → Command Bus
7. Use Case Execution → Application Layer
8. Response Serialization → Pydantic Response
9. Response → Client
```

### Middleware Stack
```python
# infrastructure/middleware/middleware.py
class MiddlewareStack:
    def __init__(self):
        self.middleware = [
            RequestIDMiddleware(),    # Correlation IDs
            LoggingMiddleware(),      # Request logging
            AuthMiddleware(),         # JWT validation
            RateLimitMiddleware(),    # Rate limiting
            ErrorHandlingMiddleware(), # Error handling
        ]
    
    async def __call__(self, request: Request, call_next):
        for middleware in self.middleware:
            request = await middleware(request, call_next)
        return await call_next(request)
```

### API Versioning
- URL versioning: `/api/v1/`, `/api/v2/`
- Header versioning: `Accept: application/vnd.quantx.v1+json`
- Deprecation timeline: 6 months minimum
- Migration guide in release notes

## Database Integration

### Repository Pattern
```python
class PositionRepository(Protocol):
    async def get_by_id(self, id: PositionId) -> Optional[Position]: ...
    async def save(self, position: Position) -> None: ...
    async def get_open_positions(
        self, 
        strategy_id: StrategyId,
    ) -> list[Position]: ...

class PostgresPositionRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool
    
    async def save(self, position: Position) -> None:
        query = """
            INSERT INTO positions (id, strategy_id, symbol, ...)
            VALUES ($1, $2, $3, ...)
            ON CONFLICT (id) DO UPDATE SET ...
        """
        await self.pool.execute(
            query,
            position.id,
            position.strategy_id,
            position.symbol.value,
            ...
        )
```

### Connection Management
```python
# infrastructure/database/connection.py
class DatabaseManager:
    def __init__(self, config: DatabaseConfig) -> None:
        self._pools: dict[str, asyncpg.Pool] = {}
    
    async def get_pool(self, name: str) -> asyncpg.Pool:
        if name not in self._pools:
            self._pools[name] = await asyncpg.create_pool(
                dsn=config.url,
                min_size=10,
                max_size=100,
            )
        return self._pools[name]
    
    async def close_all(self) -> None:
        for pool in self._pools.values():
            await pool.close()
```

## Message Queue Integration

### Event Publishing
```python
# infrastructure/events/publisher.py
class EventPublisher:
    def __init__(self, connection: aio_pika.RobustConnection) -> None:
        self.connection = connection
    
    async def publish(
        self, 
        event: DomainEvent,
    ) -> None:
        exchange = self.connection.get_exchange("events")
        await exchange.publish(
            aio_pika.Message(
                body=event.model_dump_json().encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                headers={
                    "event_type": event.__class__.__name__,
                    "correlation_id": event.correlation_id,
                },
            ),
            routing_key=event.routing_key,
        )
```

### Event Consumption
```python
# infrastructure/events/consumer.py
class EventConsumer:
    def __init__(self, connection: aio_pika.RobustConnection) -> None:
        self.connection = connection
    
    async def start(self) -> None:
        channel = await self.connection.channel()
        exchange = await channel.get_exchange("events")
        queue = await channel.declare_queue(
            "trading-service",
            durable=True,
        )
        await queue.bind(exchange, routing_key="position.*")
        await queue.bind(exchange, routing_key="order.*")
        
        await queue.consume(self._handle_message)
    
    async def _handle_message(self, message: aio_pika.IncomingMessage) -> None:
        async with message.process():
            event = parse_event(message.body)
            await self._process_event(event)
```

## Cache Integration

### Redis Cache Strategy
```python
# infrastructure/cache/redis_cache.py
class RedisCache:
    def __init__(self, redis: aioredis.Redis) -> None:
        self.redis = redis
    
    async def get_market_data(
        self, 
        symbol: Symbol,
        timeframe: Timeframe,
    ) -> Optional[MarketData]:
        key = f"market:{symbol}:{timeframe}"
        data = await self.redis.get(key)
        return MarketData(**json.loads(data)) if data else None
    
    async def set_market_data(
        self, 
        symbol: Symbol,
        timeframe: Timeframe,
        data: MarketData,
    ) -> None:
        key = f"market:{symbol}:{timeframe}"
        await self.redis.setex(
            key, 
            timedelta(seconds=60),
            json.dumps(data.model_dump()),
        )
```

### Cache Invalidation
- Time-based TTL for market data (60s)
- Manual invalidation on position changes
- Event-driven invalidation for predictions
- Cache warming on service startup

## Background Workers

### Worker Types
| Worker | Purpose | Schedule |
|--------|---------|----------|
| PositionSyncWorker | Sync open positions | Every 30s |
| OrderSyncWorker | Sync order status | Every 5s |
| PredictionWorker | Generate predictions | Ongoing |
| HealthCheckWorker | Exchange health checks | Every 60s |

### Worker Architecture
```python
# services/trading/workers/order_sync_worker.py
class OrderSyncWorker:
    def __init__(
        self,
        order_repo: OrderRepository,
        exchange_client: ExchangeClient,
    ) -> None:
        self.order_repo = order_repo
        self.exchange_client = exchange_client
    
    async def run(self) -> None:
        while True:
            pending_orders = await self.order_repo.get_pending_orders()
            for order in pending_orders:
                status = await self.exchange_client.get_order_status(
                    order.exchange_order_id
                )
                if status != OrderStatus.PENDING:
                    await self.order_repo.update_status(order.id, status)
            
            await asyncio.sleep(5)
```

## Service Communication

### Internal API Calls
```python
# clients/strategy_client.py
class StrategyClient:
    def __init__(self, base_url: str, timeout: int = 5) -> None:
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
        )
    
    async def get_strategy(
        self, 
        strategy_id: StrategyId,
    ) -> StrategyDTO:
        response = await self.client.get(f"/strategies/{strategy_id}")
        response.raise_for_status()
        return StrategyDTO(**response.json())
```

### Circuit Breaker Pattern
```python
# infrastructure/circuit_breaker/circuit_breaker.py
class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure: Optional[datetime] = None
        self.state = CircuitState.CLOSED
    
    async def call[T](
        self, 
        func: Callable[..., Awaitable[T]],
    ) -> T:
        if self._is_open():
            raise CircuitBreakerOpenError()
        
        try:
            result = await func()
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure = datetime.utcnow()
            if self.failures >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise e
```

## Configuration Management

### Environment Configuration
```python
# infrastructure/config/config.py
class ServiceConfig(BaseSettings):
    database_url: PostgresDsn
    redis_url: RedisDsn
    rabbitmq_url: AmqpDsn
    
    class Config:
        env_file = ".env"
        env_prefix = "QUANTX_"
```

### Feature Flags
```python
# infrastructure/config/feature_flags.py
class FeatureFlags:
    def __init__(self, store: FeatureFlagStore) -> None:
        self.store = store
    
    async def is_enabled(self, feature: str, user_id: UserId) -> bool:
        flags = await self.store.get_user_flags(user_id)
        return flags.get(feature, False)
```

## Error Handling

### Global Error Handler
```python
# infrastructure/errors/error_handler.py
def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationError)
    async def handle_validation_error(
        request: Request, 
        exc: ValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "message": str(exc),
                "details": exc.errors(),
            },
        )
```

### Error Categories
| Category | Handling | Retry |
|----------|----------|-------|
| Validation | Fail fast | No |
| Infrastructure | Retry + circuit breaker | Yes |
| Business Logic | Domain-specific handling | Conditional |
| External API | Retry + fallback | Yes |

## Health Checks

### Liveness Probe
```python
@app.get("/health/live")
async def liveness() -> dict:
    """Check if service is running."""
    return {"status": "alive"}
```

### Readiness Probe
```python
@app.get("/health/ready")
async def readiness() -> dict:
    """Check if service can handle requests."""
    checks = {
        "database": await database.health_check(),
        "cache": await cache.health_check(),
        "message_queue": await mq.health_check(),
    }
    
    if all(checks.values()):
        return {"status": "ready", "checks": checks}
    
    raise HTTPException(status_code=503, detail=checks)
```

## Metrics & Monitoring

### Prometheus Metrics
```python
# infrastructure/metrics/metrics.py
class TradingMetrics:
    def __init__(self) -> None:
        self.orders_placed = Counter(
            "quantx_orders_placed_total",
            "Total orders placed",
            ["exchange", "symbol", "side"],
        )
        self.order_latency = Histogram(
            "quantx_order_latency_seconds",
            "Order placement latency",
            ["exchange"],
        )
```

### OpenTelemetry Tracing
```python
# infrastructure/tracing/tracer.py
tracer = trace.get_tracer("quantx-trading")

@tracer.start_as_current_span("place_order")
async def place_order(order: Order) -> ExchangeOrder:
    span = trace.get_current_span()
    span.set_attribute("order.symbol", order.symbol.value)
    span.set_attribute("order.quantity", float(order.quantity))
    ...
```

## Logging Architecture

### Structured Logging
```python
# infrastructure/logging/logger.py
class StructuredLogger:
    def __init__(self) -> None:
        self.logger = structlog.get_logger()
    
    def info(self, message: str, **kwargs) -> None:
        self.logger.info(
            message,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs,
        )
```

### Log Levels
| Level | Usage |
|-------|-------|
| DEBUG | Development only |
| INFO | Operational events |
| WARNING | Recoverable issues |
| ERROR | Errors requiring attention |
| CRITICAL | System-threatening |

## Related Documents
- [06_CLEAN_ARCHITECTURE.md](06_CLEAN_ARCHITECTURE.md)
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [23_BACKGROUND_WORKERS.md](23_BACKGROUND_WORKERS.md)
- [29_LOGGING.md](29_LOGGING.md)
- [31_OBSERVABILITY.md](31_OBSERVABILITY.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Core Architecture*