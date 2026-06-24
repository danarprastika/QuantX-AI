# QuantX AI - Service Boundaries

## Overview

This document defines the boundaries, responsibilities, and communication patterns between services in the QuantX AI system. Services follow the Single Responsibility Principle and communicate through well-defined contracts.

## Service Catalog

| Service | Responsibility | Technology | Scale |
|---------|---------------|------------|-------|
| Trading Service | Order execution, position management | Python/FastAPI | High |
| Strategy Service | Strategy lifecycle, AI model management | Python/FastAPI | High |
| Market Data Service | Market data ingestion, processing | Python/FastAPI | Very High |
| User Auth Service | Authentication, user management | Python/FastAPI | Medium |
| Telegram Service | Bot interaction, message handling | Python/aiogram | Medium |
| Portfolio Service | Analytics, reporting | Python/FastAPI | Medium |
| Notification Service | Multi-channel notifications | Python/FastAPI | Low |

## Service Boundaries Matrix

| Service | Owns | Creates | Updates | Deletes | Queries |
|---------|-------|---------|---------|---------|---------|
| Trading | Positions, Orders | Positions, Orders | Positions, Orders | Positions, Orders | Positions, Orders |
| Strategy | Strategies, Models | Strategies | Strategies | Strategies | Strategies, Models |
| Market Data | MarketData, Tickers | MarketData | MarketData | None | MarketData |
| User Auth | Users, Sessions, APIKeys | Users | Users (limited) | Users | Users, Sessions |
| Telegram | Conversations, State | Conversations | Conversations | Conversations | Conversations |
| Portfolio | Analytics, Reports | Reports | Analytics | Reports | Analytics |
| Notification | Notifications | Notifications | Notifications | Notifications | Notifications |

## Service: Trading Service

### Responsibility
- Position lifecycle management
- Order placement and tracking
- Trade execution
- Risk limit enforcement
- Exchange order synchronization

### Bounded Context
```
Context: Trading
Ubiquitous Language: Position, Order, Execution, Fill, StopLoss, TakeProfit
```

### External Dependencies
- Strategy Service (read-only for strategy config)
- Market Data Service (market prices)
- Exchange Adapters (order placement)
- Portfolio Service (P&L updates)

### Events Published
- `PositionOpened`
- `PositionClosed`
- `OrderSubmitted`
- `OrderFilled`
- `OrderCancelled`
- `RiskLimitBreached`

### Events Consumed
- `PredictionGenerated`
- `StrategyStatusChanged`
- `MarketDataUpdated`

### API Endpoints
```
POST   /api/v1/trading/positions/{symbol}/open
POST   /api/v1/trading/positions/{symbol}/close
GET    /api/v1/trading/positions
GET    /api/v1/trading/orders/{id}
POST   /api/v1/trading/orders
DELETE /api/v1/trading/orders/{id}
```

## Service: Strategy Service

### Responsibility
- Strategy creation and configuration
- AI model training and deployment
- Strategy lifecycle (activate/pause/stop)
- Backtesting orchestration
- Strategy performance tracking

### Bounded Context
```
Context: Strategy Management
Ubiquitous Language: Strategy, Model, Backtest, Prediction, Accuracy
```

### External Dependencies
- User Auth Service (user validation)
- Trading Service (strategy activation)
- Market Data Service (historical data)

### Events Published
- `StrategyCreated`
- `StrategyActivated`
- `StrategyPaused`
- `StrategyStopped`
- `ModelTrained`
- `PredictionGenerated`
- `BacktestCompleted`

### Events Consumed
- `OrderFilled` (for performance tracking)
- `PositionClosed` (for performance tracking)

### API Endpoints
```
POST   /api/v1/strategies
GET    /api/v1/strategies
GET    /api/v1/strategies/{id}
PUT    /api/v1/strategies/{id}
DELETE /api/v1/strategies/{id}
POST   /api/v1/strategies/{id}/activate
POST   /api/v1/strategies/{id}/pause
POST   /api/v1/strategies/{id}/train
GET    /api/v1/strategies/{id}/predictions
POST   /api/v1/strategies/{id}/backtest
```

## Service: Market Data Service

### Responsibility
- Real-time market data ingestion
- Data normalization and validation
- Historical data storage
- Data quality monitoring
- Streaming to consumers

### Bounded Context
```
Context: Market Data
Ubiquitous Language: Ticker, Candle, OrderBook, Symbol, Exchange
```

### External Dependencies
- Exchange Adapters (WebSocket connections)
- Database (TimescaleDB)
- Cache (Redis)

### Events Published
- `MarketDataReceived`
- `CandleClosed`
- `TickerUpdated`
- `OrderBookUpdated`
- `DataQualityAlert`

### Events Consumed
- `StrategyCreated` (to subscribe to symbols)
- `ExchangeConnected`

### API Endpoints
```
GET    /api/v1/market-data/tickers/{symbol}
GET    /api/v1/market-data/candles/{symbol}
GET    /api/v1/market-data/orderbook/{symbol}
GET    /api/v1/market-data/stream/{symbol}
POST   /api/v1/market-data/subscriptions
DELETE /api/v1/market-data/subscriptions/{symbol}
```

## Service: User Auth Service

### Responsibility
- User registration and authentication
- API key management
- Exchange credential storage
- Subscription management
- Session handling

### Bounded Context
```
Context: User Management
Ubiquitous Language: User, APIKey, Subscription, Session, Credentials
```

### External Dependencies
- Database (PostgreSQL)
- Cache (Redis)
- Vault (Secrets)

### Events Published
- `UserRegistered`
- `UserVerified`
- `APIKeyCreated`
- `SubscriptionActivated`
- `SubscriptionExpired`
- `CredentialsUpdated`

### Events Consumed
- None (foundational service)

### API Endpoints
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/api-keys
GET    /api/v1/auth/me
PUT    /api/v1/auth/credentials
DELETE /api/v1/auth/api-keys/{id}
GET    /api/v1/auth/subscriptions
```

## Service: Telegram Service

### Responsibility
- Bot command handling
- Message formatting
- Conversation state management
- User notification delivery
- Interactive configuration

### Bounded Context
```
Context: User Interface
Ubiquitous Language: Command, Message, Conversation, Handler, InlineButton
```

### External Dependencies
- Strategy Service (strategy commands)
- Trading Service (position queries)
- User Auth Service (user validation)
- Notification Service (message queuing)

### Events Published
- `TelegramCommandReceived`
- `TelegramMessageSent`

### Events Consumed
- `PositionOpened`
- `PositionClosed`
- `OrderFilled`
- `PredictionGenerated`
- `RiskLimitBreached`

### Telegram Commands
```
/start - Register or welcome user
/help - Show available commands
/create_strategy - Start strategy creation wizard
/list_strategies - Show user's strategies
/activate_strategy - Activate a strategy
/pause_strategy - Pause a strategy
/positions - Show open positions
/performance - Show strategy performance
/settings - Configure user settings
```

## Service: Portfolio Service

### Responsibility
- Portfolio valuation
- Performance analytics
- Risk exposure calculation
- Reporting generation
- P&L aggregation

### Bounded Context
```
Context: Portfolio Analytics
Ubiquitous Language: Portfolio, PnL, Exposure, Report, Benchmark
```

### External Dependencies
- Trading Service (positions, orders)
- Strategy Service (strategy info)
- User Auth Service (user info)

### Events Published
- `PortfolioValued`
- `PerformanceCalculated`
- `ReportGenerated`
- `ExposureWarning`

### Events Consumed
- `PositionOpened`
- `PositionClosed`
- `OrderFilled`
- `StrategyActivated`

### API Endpoints
```
GET    /api/v1/portfolio/value
GET    /api/v1/portfolio/performance
GET    /api/v1/portfolio/exposure
GET    /api/v1/portfolio/reports
POST   /api/v1/portfolio/reports/generate
```

## Service: Notification Service

### Responsibility
- Multi-channel notification delivery
- Template management
- Notification queuing
- Delivery status tracking

### Bounded Context
```
Context: Notification
Ubiquitous Language: Notification, Template, Delivery, Channel, Status
```

### External Dependencies
- Telegram Service (Telegram delivery)
- Email service (future)
- SMS service (future)

### Events Published
- `NotificationSent`
- `NotificationFailed`

### Events Consumed
- All domain events requiring user notification

### API Endpoints
```
POST   /api/v1/notifications
GET    /api/v1/notifications/status/{id}
GET    /api/v1/notifications/templates
```

## Service Communication Patterns

### Synchronous Communication
- Direct API calls for request-response
- Circuit breaker pattern for resilience
- Retry with exponential backoff
- Timeout enforcement (5s default)

### Asynchronous Communication
- Event-driven via message queue
- At-least-once delivery guarantee
- Idempotent event handlers
- Dead letter queue for failures

### Data Flow Patterns

#### Strategy Creation Flow
```
Telegram → User Auth → Strategy Service → Trading Service
   ↓           ↓            ↓             ↓
Command    Validate    Create Strategy    Subscribe
   ↓           ↓            ↓             ↓
Response ← Query ← StrategyCreated Event ← Market Data
```

#### Order Execution Flow
```
Market Data → Strategy Service → Trading Service → Exchange
     ↓             ↓                ↓           ↓
Prediction   Signal Evaluated   Order Placed   Execution
     ↓             ↓                ↓           ↓
Event      OrderSubmitted Event   OrderFilled Event   Position Updated
```

## Service Contracts

### Command Contracts
```json
{
  "command": "CreateStrategy",
  "correlation_id": "uuid",
  "user_id": "uuid",
  "payload": {
    "name": "string",
    "type": "enum",
    "config": {}
  },
  "timestamp": "ISO8601"
}
```

### Event Contracts
```json
{
  "event": "PositionOpened",
  "event_id": "uuid",
  "correlation_id": "uuid",
  "position_id": "uuid",
  "payload": {
    "strategy_id": "uuid",
    "symbol": "string",
    "side": "BUY/SELL",
    "quantity": "decimal"
  },
  "timestamp": "ISO8601",
  "version": "1.0"
}
```

### API Contracts
All APIs follow RESTful conventions with:
- OpenAPI 3.0 specification
- JSON request/response bodies
- JWT authentication
- Rate limiting headers

## Service Deployment Considerations

### Statelessness
- All services except Market Data are stateless
- Market Data maintains WebSocket connections
- Session state stored in Redis

### Scaling Strategy
| Service | Scaling Method | Reason |
|---------|---------------|--------|
| Trading | Horizontal | More users, more orders |
| Strategy | Vertical + Horizontal | Model inference intensive |
| Market Data | Horizontal by Symbol | Stream processing |
| User Auth | Vertical | Low CPU, high consistency |
| Telegram | Horizontal | Message throughput |
| Portfolio | Vertical | Heavy queries |
| Notification | Horizontal by Channel | Delivery throughput |

### Data Locality
- Trading Service and PostgreSQL co-located
- Market Data and Redis/TimescaleDB co-located
- User Auth and PostgreSQL co-located

## Related Documents
- [02_SYSTEM_ARCHITECTURE.md](02_SYSTEM_ARCHITECTURE.md)
- [06_CLEAN_ARCHITECTURE.md](06_CLEAN_ARCHITECTURE.md)
- [22_BACKEND_ARCHITECTURE.md](22_BACKEND_ARCHITECTURE.md)
- [11_API_SPECIFICATION.md](11_API_SPECIFICATION.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Core Architecture*