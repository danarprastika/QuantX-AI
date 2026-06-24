# QuantX AI - Domain Model

## Overview

This document defines the core domain entities, value objects, aggregates, and domain services for QuantX AI. The domain model follows Domain-Driven Design (DDD) principles and Clean Architecture patterns.

## Domain Context Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           QuantX AI Bounded Contexts                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │   TRADING    │  │  STRATEGY    │  │   MARKET     │  │    USER      │   │
│   │              │  │              │  │    DATA      │  │              │   │
│   │ Positions    │  │ Strategies   │  │ Market Data  │  │ Users        │   │
│   │ Orders       │  │ Backtests    │  │ Tickers      │  │ Subscriptions│   │
│   │ Executions   │  │ Models       │  │ Candles      │  │ Sessions     │   │
│   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Entities

### User Aggregate

```
User (Aggregate Root)
├── id: UserId
├── telegram_id: TelegramId
├── email: Email
├── subscription: Subscription
├── preferences: UserPreferences
├── created_at: DateTime
└── updated_at: DateTime
```

**Invariants**:
- Email must be unique across system
- Telegram ID must be unique
- Cannot deactivate active subscription without grace period

### Strategy Aggregate

```
Strategy (Aggregate Root)
├── id: StrategyId
├── user_id: UserId
├── name: StrategyName
├── type: StrategyType
├── config: StrategyConfig
├── model_version: ModelVersion
├── status: StrategyStatus
├── created_at: DateTime
├── updated_at: DateTime
└── positions: List<PositionId>
```

**Invariants**:
- Name cannot exceed 100 characters
- Only one active strategy per symbol per user (configurable)
- Status transitions follow defined workflow

### Position Aggregate

```
Position (Aggregate Root)
├── id: PositionId
├── strategy_id: StrategyId
├── symbol: Symbol
├── side: Side
├── quantity: Decimal
├── entry_price: Price
├── exit_price: Optional<Price>
├── status: PositionStatus
├── opened_at: DateTime
├── closed_at: Optional<DateTime>
├── stop_loss: Optional<Price>
└── take_profit: Optional<Price>
```

**Invariants**:
- Position quantity must be positive
- Entry price must be positive
- Closed positions must have exit price
- Stop loss must be below entry for long positions

### Order Aggregate

```
Order (Aggregate Root)
├── id: OrderId
├── position_id: PositionId
├── symbol: Symbol
├── side: Side
├── type: OrderType
├── quantity: Decimal
├── price: Optional<Price>
├── status: OrderStatus
├── exchange_order_id: Optional[str]
├── created_at: DateTime
└── updated_at: DateTime
```

**Invariants**:
- Market orders have no price
- Limit orders require price
- Quantity must match position requirements

### Prediction Aggregate

```
Prediction (Aggregate Root)
├── id: PredictionId
├── strategy_id: StrategyId
├── symbol: Symbol
├── timeframe: Timeframe
├── predicted_at: DateTime
├── target_at: DateTime
├── confidence: ConfidenceScore
├── predicted_price: Price
├── actual_price: Optional<Price>
└── accuracy: Optional[float]
```

**Invariants**:
- Confidence must be between 0 and 1
- Predicted price must be positive
- Target time must be after predicted time

## Value Objects

### Symbol
```
Symbol
├── base: str (3-10 uppercase letters)
├── quote: str (3-5 uppercase letters)
└── format: str (e.g., "BTCUSDT")
```
**Validation**: Must follow standard exchange format

### Money
```
Money
├── amount: Decimal
├── currency: CurrencyCode
└── __add__, __sub__ with currency validation
```

### Price
```
Price: Money
└── Must be positive, max 8 decimal places
```

### Side
```
enum Side:
    BUY = "BUY"
    SELL = "SELL"
```

### Timeframe
```
enum Timeframe:
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
```

### StrategyType
```
enum StrategyType:
    LSTM_PREDICTION = "lstm_prediction"
    TRANSFORMER = "transformer"
    ENSEMBLE = "ensemble"
    RSI_MOMENTUM = "rsi_momentum"
    MOVING_AVERAGE = "moving_average"
```

### StrategyStatus
```
enum StrategyStatus:
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    ARCHIVED = "archived"
```

### PositionStatus
```
enum PositionStatus:
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"
```

### OrderStatus
```
enum OrderStatus:
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
```

## Domain Events

### User Events
- `UserCreated`: New user registered
- `UserUpdated`: User profile updated
- `SubscriptionActivated`: Subscription started
- `SubscriptionExpired`: Subscription ended

### Strategy Events
- `StrategyCreated`: Strategy defined
- `StrategyActivated`: Strategy started
- `StrategyPaused`: Strategy suspended
- `StrategyStopped`: Strategy terminated
- `StrategyConfigChanged`: Configuration updated

### Position Events
- `PositionOpened`: New position created
- `PositionClosed`: Position exited
- `PositionModified`: Stop loss/take profit updated

### Order Events
- `OrderSubmitted`: Order sent to exchange
- `OrderFilled`: Order completely filled
- `OrderCancelled`: Order cancelled
- `OrderRejected`: Exchange rejected order

### Prediction Events
- `PredictionGenerated`: AI model produced prediction
- `PredictionValidated`: Prediction accuracy calculated

## Domain Services

### StrategyValidationService
Validates strategy configuration and feasibility:
- Check symbol availability
- Validate timeframe compatibility
- Verify risk parameters

### RiskCalculationService
Calculates risk metrics:
- Position size
- Stop loss levels
- Portfolio exposure

### OrderValidationService
Validates order parameters:
- Balance sufficiency
- Exchange rules compliance
- Risk limit adherence

### PerformanceCalculationService
Calculates trading metrics:
- Profit/Loss
- Sharpe ratio
- Drawdown
- Win rate

## Aggregates Relationships

```
User 1 ── * Strategy
Strategy 1 ── * Position
Position 1 ── * Order
Strategy 1 ── * Prediction
Order 0..1 ── 1 Position
Prediction 0..1 ── 1 Position (when realized)
```

## Repository Interfaces

### UserRepository
```python
class UserRepository(Protocol):
    def get_by_id(self, id: UserId) -> Optional[User]: ...
    def get_by_telegram_id(self, telegram_id: TelegramId) -> Optional[User]: ...
    def save(self, user: User) -> None: ...
    def delete(self, id: UserId) -> None: ...
```

### StrategyRepository
```python
class StrategyRepository(Protocol):
    def get_by_id(self, id: StrategyId) -> Optional[Strategy]: ...
    def get_active_for_user(self, user_id: UserId) -> list[Strategy]: ...
    def get_by_symbol(self, symbol: Symbol) -> list[Strategy]: ...
    def save(self, strategy: Strategy) -> None: ...
```

### PositionRepository
```python
class PositionRepository(Protocol):
    def get_open_positions(self, strategy_id: StrategyId) -> list[Position]: ...
    def get_by_id(self, id: PositionId) -> Optional[Position]: ...
    def save(self, position: Position) -> None: ...
```

### OrderRepository
```python
class OrderRepository(Protocol):
    def get_pending_orders(self) -> list[Order]: ...
    def get_by_exchange_id(self, exchange_id: str) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...
```

## Domain Invariants by Aggregate

### User Invariants
1. Unique email enforcement across system
2. Subscription cannot be created if another active subscription exists
3. User cannot place orders without valid subscription

### Strategy Invariants
1. Name length limited to 100 characters
2. Cannot transition to ACTIVE without valid exchange API keys
3. Config changes require validation before saving
4. At most one ACTIVE strategy per symbol per user (configurable rule)

### Position Invariants
1. Quantity must be positive and within exchange limits
2. Entry price must be positive
3. Stop loss must be valid for position side
4. Cannot modify closed position
5. Take profit must be above entry for long positions

### Order Invariants
1. Market orders require quantity only
2. Limit orders require both price and quantity
3. Order quantity cannot exceed position remaining quantity
4. Cannot cancel filled order
5. Exchange order ID must be unique per exchange

## Entity Lifecycle

### Strategy Lifecycle
```
DRAFT → ACTIVE → PAUSED ↔ ACTIVE → STOPPED → ARCHIVED
                ↘____________↗
```

### Position Lifecycle
```
OPEN → (CLOSED | CANCELLED)
```

### Order Lifecycle
```
PENDING → SUBMITTED → (FILLED | PARTIALLY_FILLED → FILLED | REJECTED)
              ↓
         CANCELLED (before filled)
```

## Business Rules

### Risk Management
1. **Maximum Position Size**: Configurable per strategy (default: 5% portfolio)
2. **Maximum Concurrent Positions**: Configurable per user (default: 10)
3. **Daily Loss Limit**: Configurable per strategy (default: 10% equity)
4. **Minimum Confidence**: Predictions below threshold are ignored (default: 0.6)

### Exchange Rules
1. **Rate Limits**: Per-exchange request throttling
2. **Order Symbols**: Only whitelisted symbols allowed
3. **Minimum Quantity**: Exchange-specific minimum order sizes

### Subscription Rules
1. **Active Strategies**: Limited by subscription tier
2. **API Calls**: Throttling based on subscription level
3. **Features**: Advanced features gated by tier

## Related Documents
- [06_CLEAN_ARCHITECTURE.md](06_CLEAN_ARCHITECTURE.md)
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [08_DATABASE_DESIGN.md](08_DATABASE_DESIGN.md)
- [09_DATABASE_SCHEMA.md](09_DATABASE_SCHEMA.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Foundation*