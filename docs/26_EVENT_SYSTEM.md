---
status: Approved
owner: Backend Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/26_EVENT_SYSTEM.md
depends_on:
  - docs/12_API_CONTRACTS.md
  - docs/24_MESSAGE_QUEUE.md
  - docs/30_MONITORING.md
related_documents:
  - docs/12_API_CONTRACTS.md
  - docs/24_MESSAGE_QUEUE.md
  - docs/30_MONITORING.md
---
# QuantX AI - Event System

## Overview

This document defines the event-driven architecture for QuantX AI, including event types, schemas, publishing patterns, consumption patterns, and event sourcing considerations.

## Event Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Event System Architecture                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │   Strategy   │  │   Trading    │  │   Market     │  │   User       │ │
│   │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼─────────────────────────────────────────────────────────────┐    │
│   │                    Event Bus (RabbitMQ)                             │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │    │
│   │  │ Strategy │  │ Trading  │  │ Market   │  │ User     │         │    │
│   │  │ Events   │  │ Events   │  │ Events   │  │ Events   │         │    │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Portfolio  │  │   Telegram   │  │   Notifica-  │  │   Analytics  │ │
│  │   Service    │  │   Service    │  │   tions      │  │   Service    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Event Types

### Strategy Events
| Event | Trigger | Payload |
|-------|---------|---------|
| StrategyCreated | New strategy | Strategy details |
| StrategyActivated | Activation | Activated parameters |
| StrategyPaused | Pause command | Reason |
| StrategyStopped | Stop command | Closing positions |
| StrategyConfigChanged | Config update | New config |
| ModelTrained | Model training complete | Model version |
| PredictionGenerated | AI prediction | Prediction data |
| BacktestCompleted | Backtest finish | Results |

### Trading Events
| Event | Trigger | Payload |
|-------|---------|---------|
| PositionOpened | Order filled | Position details |
| PositionClosed | Position closed | Exit details |
| PositionModified | SL/TP change | New values |
| OrderSubmitted | Order created | Order details |
| OrderFilled | Partial/full fill | Fill details |
| OrderCancelled | Cancellation | Reason |
| OrderRejected | Exchange reject | Rejection reason |
| RiskLimitBreached | Risk violation | Violation details |

### Market Events
| Event | Trigger | Payload |
|-------|---------|---------|
| MarketDataReceived | New price | Price data |
| CandleClosed | Candle end | Candle data |
| OrderBookUpdated | Order book change | OB snapshot |
| DataQualityAlert | Data issue | Alert details |

### User Events
| Event | Trigger | Payload |
|-------|---------|---------|
| UserRegistered | Registration | User data |
| UserVerified | Confirmation | Verification |
| APIKeyCreated | Key creation | Key ID |
| APIKeyDeleted | Key deletion | Key ID |
| SubscriptionActivated | Payment | Subscription data |
| SubscriptionExpired | Expiration | Expiry date |
| CredentialsUpdated | Exchange keys | Exchange info |

## Event Schema

### Base Event Structure
```python
class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    correlation_id: UUID
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: dict
    version: str = "1.0"
    metadata: dict = Field(default_factory=dict)
    
    @property
    def routing_key(self) -> str:
        return self.event_type.lower()
```

### Versioned Event Schema
```python
class EventSchema(BaseModel):
    name: str
    version: str
    schema: dict  # JSON Schema
    compatibility: str  # "backward", "forward", "none"
    deprecated: bool = False
```

## Event Publishing

### Event Bus Interface
```python
class EventBus(Protocol):
    async def publish(self, event: DomainEvent) -> None: ...
    async def publish_batch(self, events: list[DomainEvent]) -> None: ...
    async def subscribe(
        self, 
        handler: Callable[[DomainEvent], Awaitable[None]],
        event_types: list[str],
    ) -> None: ...
```

### Publishing Pattern
```python
class EventPublisher:
    def __init__(self, bus: EventBus) -> None:
        self.bus = bus
    
    async def publish_strategy_created(
        self,
        strategy: Strategy,
    ) -> None:
        event = StrategyCreated(
            strategy_id=strategy.id,
            user_id=strategy.user_id,
            strategy_type=strategy.type,
            symbol=strategy.symbol,
            correlation_id=strategy.id,
        )
        await self.bus.publish(event)
```

## Event Consumption

### Handler Registration
```python
class EventHandlerRegistry:
    def __init__(self) -> None:
        self.handlers: dict[str, list[EventHandler]] = {}
    
    def register(
        self,
        event_type: str,
        handler: EventHandler,
    ) -> None:
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
```

### Consumer Pattern
```python
@event_handler("prediction_generated")
async def handle_prediction_generated(
    event: PredictionGenerated,
) -> None:
    strategy = await strategy_repo.get(event.strategy_id)
    if strategy.status == StrategyStatus.ACTIVE:
        signal = Signal(
            strategy_id=strategy.id,
            action=derive_action(event),
            confidence=event.confidence,
        )
        await signal_queue.enqueue(signal)
```

## Event Sourcing Considerations

### Outbox Pattern
```sql
CREATE TABLE strategy_outbox (
    id UUID PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE
);

-- Process outbox with transaction
BEGIN;
INSERT INTO strategies ...;
INSERT INTO strategy_outbox (event_type, payload) VALUES ('StrategyCreated', ...);
COMMIT;

-- Background process publishes events
SELECT * FROM strategy_outbox WHERE NOT processed;
```

### Idempotency
```python
class IdempotentEventHandler:
    def __init__(self, event_store: EventStore) -> None:
        self.event_store = event_store
    
    async def handle(self, event: DomainEvent) -> None:
        # Check if already processed
        if await self.event_store.already_processed(event.event_id):
            return
        
        # Process and record
        await self.process(event)
        await self.event_store.mark_processed(event.event_id)
```

## Event Retention

### TTL Policy
| Event Type | Retention | Reason |
|------------|-----------|--------|
| User Events | 30 days | Compliance |
| Strategy Events | 90 days | Analytics |
| Trading Events | 7 years | Audit |
| Market Events | 30 days | Volume |

### Archival
- Events archived to MongoDB
- Compressed after 30 days
- Indexed for querying
- Deleted after retention period

## Related Documents
- [12_API_CONTRACTS.md](12_API_CONTRACTS.md)
- [24_MESSAGE_QUEUE.md](24_MESSAGE_QUEUE.md)
- [30_MONITORING.md](30_MONITORING.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Backend Team*
*Source of Truth: docs/26_EVENT_SYSTEM.md*
*Depends On: 12_API_CONTRACTS.md, 24_MESSAGE_QUEUE.md, 30_MONITORING.md*
*Related Documents: 12_API_CONTRACTS.md, 24_MESSAGE_QUEUE.md, 30_MONITORING.md*
*Phase: Infrastructure*
