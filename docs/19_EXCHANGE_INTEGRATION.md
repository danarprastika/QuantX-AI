---
status: Approved
owner: Backend Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/19_EXCHANGE_INTEGRATION.md
depends_on:
  - docs/07_SERVICE_BOUNDARIES.md
  - docs/17_AI_ARCHITECTURE.md
  - docs/22_BACKEND_ARCHITECTURE.md
  - docs/31_OBSERVABILITY.md
related_documents:
  - docs/07_SERVICE_BOUNDARIES.md
  - docs/17_AI_ARCHITECTURE.md
  - docs/22_BACKEND_ARCHITECTURE.md
  - docs/31_OBSERVABILITY.md
---
# QuantX AI - Exchange Integration

## Overview

This document describes the architecture for integrating with cryptocurrency exchanges including Binance, Coinbase Pro, Kraken, and FTX. The integration layer provides unified access to exchange functionality while handling rate limits, reliability, and data consistency.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Exchange Integration Layers                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │  Exchange    │  │   Trading    │  │   Market     │  │    Data      │ │
│   │  Registry    │  │   Adapter    │  │   Adapter    │  │   Adapter    │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐ │
│   │   Unified    │  │   Unified    │  │   Unified    │  │   Unified    │ │
│   │   Exchange   │  │   Order      │  │   Market     │  │   Data       │ │
│   │   Client     │  │   Client     │  │   Client     │  │   Client     │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼────────────────────────────────────────────────────────▼───────┐
│   │                      Concrete Implementations                           │
│   │  ┌──────────┐ ┌────────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐ │
│   │  │ Binance  │ │ Coinbase   │ │ Kraken   │ │ FTX        │ │ Mock     │ │
│   │  │ Adapter  │ │ Adapter    │ │ Adapter  │ │ Adapter    │ │ Exchange │ │
│   │  └──────────┘ └────────────┘ └──────────┘ └────────────┘ └──────────┘ │
│   └────────────────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────────┘
```

## Exchange Client Interfaces

### ExchangeClient Protocol
```python
class ExchangeClient(Protocol):
    """Unified interface for all exchange operations."""
    
    async def get_market_data(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
    ) -> MarketData: ...
    
    async def place_order(
        self,
        order: OrderRequest,
    ) -> ExchangeOrder: ...
    
    async def cancel_order(
        self,
        order_id: ExchangeOrderId,
    ) -> None: ...
    
    async def get_order_status(
        self,
        order_id: ExchangeOrderId,
    ) -> OrderStatus: ...
    
    async def get_account_balance(
        self,
    ) -> AccountBalance: ...
    
    async def stream_market_data(
        self,
        symbol: Symbol,
    ) -> AsyncIterator[MarketUpdate]: ...
```

### Order Types Support
| Exchange | Market | Limit | Stop | StopLimit | Trailing |
|----------|--------|-------|------|-----------|----------|
| Binance | ✓ | ✓ | ✓ | ✓ | ✓ |
| Coinbase | ✓ | ✓ | ✓ | ✓ | ✗ |
| Kraken | ✓ | ✓ | ✓ | ✓ | ✗ |
| FTX | ✓ | ✓ | ✓ | ✓ | ✓ |

## Concrete Implementations

### Binance Adapter
- **Base URL**: `https://api.binance.com`
- **WebSocket**: `wss://stream.binance.com:9443`
- **Rate Limit**: 1200 requests/minute, 5000 weight/minute
- **Authentication**: HMAC-SHA256

### Coinbase Pro Adapter
- **Base URL**: `https://api.exchange.coinbase.com`
- **WebSocket**: `wss://ws-feed.exchange.coinbase.com`
- **Rate Limit**: 10 requests/second
- **Authentication**: JWT

### Kraken Adapter
- **Base URL**: `https://api.kraken.com`
- **WebSocket**: `wss://ws.kraken.com`
- **Rate Limit**: 60 requests/minute
- **Authentication**: HMAC-SHA512-SHA256

### FTX Adapter
- **Base URL**: `https://ftx.com/api`
- **WebSocket**: `wss://ftx.com/ws`
- **Rate Limit**: 300 requests/second
- **Authentication**: HMAC-SHA256

## Rate Limit Management

### Token Bucket Algorithm
```python
class RateLimiter:
    def __init__(self, rate: int, capacity: int) -> None:
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.monotonic()
    
    async def acquire(self) -> None:
        """Wait until token available."""
        ...
```

### Request Queuing
- Per-exchange request queues
- Priority for order execution over market data
- Exponential backoff on rate limit errors
- Dead letter queue for failed requests

## Reliability Patterns

### Retry Strategy
- **Exponential Backoff**: 1s, 2s, 4s, 8s (max 30s)
- **Jitter**: Random delay to prevent thundering herd
- **Max Retries**: 3 attempts for market data, 5 for orders
- **Circuit Breaker**: Open after 5 consecutive failures

### Circuit Breaker
```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int, timeout: int) -> None:
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
    
    async def call(self, func: Callable) -> Any:
        """Execute with circuit breaker protection."""
        ...
```

### Health Checks
- REST endpoint `/health` for each exchange
- WebSocket ping/pong monitoring
- Automatic failover to backup exchange
- Degradation to cached data when all fail

## Data Normalization

### Unified Symbol Format
```
Exchange Symbol → QuantX Symbol
Binance: BTCUSDT → BTC/USD
Coinbase: BTC-USD → BTC/USD
Kraken: XBT/USD → BTC/USD
FTX: BTC/USD → BTC/USD
```

### Price and Quantity Normalization
- All prices in quote currency (USD)
- Quantities in base currency (BTC)
- Decimal precision standardized to 8 places
- Timestamp normalized to UTC ISO format

### Order Status Mapping
```python
ORDER_STATUS_MAP = {
    'NEW': OrderStatus.PENDING,
    'PARTIALLY_FILLED': OrderStatus.PARTIALLY_FILLED,
    'FILLED': OrderStatus.FILLED,
    'CANCELED': OrderStatus.CANCELLED,
    'REJECTED': OrderStatus.REJECTED,
    'EXPIRED': OrderStatus.CANCELLED,
}
```

## WebSocket Management

### Connection Pooling
- Dedicated connection per exchange
- Symbol subscriptions multiplexed
- Automatic reconnect with backoff
- Connection health monitoring

### Message Throughput
- Buffer incoming messages
- Process in batches of 100
- Drop oldest when buffer full
- Alert on sustained high throughput

### Stream Resilience
- Resubscribe on reconnect
- Gap detection via sequence numbers
- Backfill missing data
- Dual connection for critical symbols

## Authentication & Security

### Credential Storage
- Encrypted at rest using Vault
- In-memory only during operation
- Rotated every 90 days
- Audit trail on access

### Signature Generation
```python
def generate_signature(
    secret: str,
    timestamp: int,
    method: str,
    path: str,
    body: Optional[str] = None,
) -> str:
    """Generate HMAC signature for exchange request."""
    ...
```

### IP Whitelist
- Exchange API access restricted to known IPs
- VPN tunnel for production
- Dynamic IP management for cloud providers

## Error Handling

### Exchange Error Categories
| Category | Examples | Handling |
|----------|----------|----------|
| Network | Timeout, connection refused | Retry with backoff |
| Rate Limit | HTTP 429, 418 | Queue and delay |
| Invalid | Bad symbol, invalid price | Fail fast |
| Account | Insufficient funds, suspended | User notification |
| System | Maintenance, outage | Circuit breaker |

### Error Codes Mapping
```python
BINANCE_ERRORS = {
    -1003: InsufficientBalanceError,
    -2019: MarginNotSatisfiedError,
    -1121: InvalidSymbolError,
}

def map_exchange_error(exchange: Exchange, code: int) -> ExchangeError:
    """Map exchange-specific error to domain error."""
    ...
```

## Fault Tolerance

### Exchange Failover
```
Primary Exchange (Binance)
      ↓ (Failure)
Secondary Exchange (Coinbase)
      ↓ (Failure)
Tertiary Exchange (Kraken)
      ↓ (Failure)
System Degraded - No Market Access
```

### Data Replication
- Market data mirrored across exchanges
- Fallback to alternative exchange for same symbol
- Consistency checks between exchange data sources
- Alert on price divergence > 1%

## Performance Requirements

### Latency Targets
| Operation | Target | SLA |
|-----------|--------|-----|
| REST Request | <50ms | <100ms |
| WebSocket Message | <10ms | <20ms |
| Order Placement | <50ms | <100ms |
| Order Status | <30ms | <50ms |

### Throughput Targets
- 1000 orders/second peak
- 100k market updates/second
- 10k concurrent WebSocket streams

## Data Synchronization

### Account Synchronization
- Hourly sync of account balances
- Real-time position sync via WebSocket
- Reconciliation daily at 00:00 UTC
- Mismatch triggers alert

### Order Synchronization
- Poll order status every 5 seconds
- WebSocket updates for fills
- Manual reconciliation for discrepancies
- Audit trail preserved

## Testing Strategy

### Mock Exchange
- Simulates all exchange behaviors
- Configurable response patterns
- Rate limit simulation
- Error injection for testing

### Sandbox Testing
- Binance testnet
- Coinbase Pro sandbox
- FTX test account
- Kraken demo environment

### Integration Testing
- Contract tests against real exchange
- No actual money movement
- Small order sizes (< $1)

## Monitoring & Observability

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| API Latency | Exchange response time | >100ms |
| Error Rate | Failed requests | >1% |
| Rate Limit Hits | Throttled requests | >10/hour |
| Order Failures | Rejected orders | >0.1% |

### Logs
- Request/response logging (sanitized)
- Error chain preservation
- Correlation IDs for tracing
- No credential logging

## Related Documents
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [17_AI_ARCHITECTURE.md](17_AI_ARCHITECTURE.md)
- [22_BACKEND_ARCHITECTURE.md](22_BACKEND_ARCHITECTURE.md)
- [31_OBSERVABILITY.md](31_OBSERVABILITY.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Backend Team*
*Source of Truth: docs/19_EXCHANGE_INTEGRATION.md*
*Depends On: 07_SERVICE_BOUNDARIES.md, 17_AI_ARCHITECTURE.md, 22_BACKEND_ARCHITECTURE.md, 31_OBSERVABILITY.md*
*Related Documents: 07_SERVICE_BOUNDARIES.md, 17_AI_ARCHITECTURE.md, 22_BACKEND_ARCHITECTURE.md, 31_OBSERVABILITY.md*
*Phase: Core Architecture*
