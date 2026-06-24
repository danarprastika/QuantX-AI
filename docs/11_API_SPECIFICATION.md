# QuantX AI - API Specification

## Overview

This document defines the RESTful API specification for QuantX AI services, including endpoint definitions, request/response schemas, authentication, error handling, and versioning strategy.

## API Architecture

### Gateway Pattern
```
Client → API Gateway (Traefik) → Service Router → FastAPI Service → Database
```

### Multi-API Design
| API Type | Port | Purpose | Authentication |
|----------|------|---------|---------------|
| User API | 8001 | User management, auth | JWT |
| Trading API | 8002 | Positions, orders | JWT |
| Strategy API | 8003 | Strategies, predictions | JWT |
| Market Data API | 8004 | Market feeds, candles | None/API Key |
| Telegram API | 8005 | Bot webhooks | Telegram signature |

## Authentication

### JWT Token Format
```
Authorization: Bearer <token>
```

**Token Structure**:
- Header: `{"alg": "HS256", "typ": "JWT"}`
- Payload: `{"sub": "user_id", "iat": timestamp, "exp": timestamp, "tiers": []}`
- Signature: HMAC-SHA256

### Token Refresh
- Access token: 15 minutes expiry
- Refresh token: 7 days expiry
- Automatic refresh on 401 response

## Rate Limiting

### Limits by Endpoint
| Endpoint Pattern | Anonymous | Authenticated | Premium |
|------------------|-----------|--------------|---------|
| /api/v1/* | 10/min | 100/min | 1000/min |
| /api/v1/trading/* | N/A | 20/min | 100/min |
| /api/v1/market/* | 1000/min | 5000/min | 10000/min |

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 2024-01-01T00:01:00Z
Retry-After: 30
```

## Error Response Format

### Standard Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "risk_limit",
        "error": "Must be between 0 and 10000"
      }
    ],
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 422 | Input validation failed |
| AUTHENTICATION_REQUIRED | 401 | Missing or invalid token |
| AUTHORIZATION_FAILED | 403 | Insufficient permissions |
| RESOURCE_NOT_FOUND | 404 | Entity not found |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Unexpected server error |
| SERVICE_UNAVAILABLE | 503 | Dependency unavailable |

## User Service API

### POST /api/v1/auth/register
Register a new user.

**Request**:
```json
{
  "telegram_id": 123456789,
  "email": "user@example.com",
  "display_name": "Optional Name"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "telegram_id": 123456789,
  "email": "user@example.com",
  "subscription_tier": "free",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### POST /api/v1/auth/login
Authenticate and receive JWT token.

**Request**:
```json
{
  "telegram_id": 123456789
}
```

**Response** (200):
```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "expires_in": 900,
  "token_type": "Bearer"
}
```

### GET /api/v1/users/me
Get current user profile.

**Response** (200):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "display_name": "User Name",
  "subscription_tier": "premium",
  "subscription_expires": "2024-12-31T23:59:59Z",
  "preferences": {
    "quiet_hours": ["22:00", "07:00"],
    "notification_channels": ["telegram", "email"]
  }
}
```

## Strategy Service API

### POST /api/v1/strategies
Create a new trading strategy.

**Request**:
```json
{
  "name": "My Strategy",
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "type": "lstm_prediction",
  "config": {
    "risk_limit": 100.00,
    "stop_loss_pct": 2.0,
    "take_profit_pct": 4.0,
    "confidence_threshold": 0.6
  }
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "My Strategy",
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "type": "lstm_prediction",
  "config": {
    "risk_limit": 100.00,
    "stop_loss_pct": 2.0,
    "take_profit_pct": 4.0,
    "confidence_threshold": 0.6
  },
  "status": "draft",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /api/v1/strategies
List user's strategies.

**Query Parameters**:
- `status` (optional): Filter by status
- `limit` (default: 50): Page size
- `offset`: Pagination offset

**Response** (200):
```json
{
  "strategies": [
    {
      "id": "uuid",
      "name": "Strategy 1",
      "symbol": "BTCUSDT",
      "status": "active",
      "performance_score": 0.65
    }
  ],
  "total": 5,
  "limit": 50,
  "offset": 0
}
```

### POST /api/v1/strategies/{id}/activate
Activate a strategy.

**Response** (200):
```json
{
  "id": "uuid",
  "status": "active",
  "activated_at": "2024-01-01T00:00:00Z"
}
```

### POST /api/v1/strategies/{id}/backtest
Run a backtest for the strategy.

**Request**:
```json
{
  "start_date": "2023-01-01T00:00:00Z",
  "end_date": "2023-12-31T23:59:59Z"
}
```

**Response** (200, long-running):
```json
{
  "backtest_id": "uuid",
  "status": "running",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Trading Service API

### POST /api/v1/trading/positions
Open a new position.

**Request**:
```json
{
  "strategy_id": "uuid",
  "symbol": "BTCUSDT",
  "side": "buy",
  "quantity": 0.01,
  "price": 50000.00,
  "stop_loss": 49000.00,
  "take_profit": 52000.00
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "strategy_id": "uuid",
  "symbol": "BTCUSDT",
  "side": "buy",
  "quantity": 0.01,
  "entry_price": 50000.00,
  "stop_loss_price": 49000.00,
  "take_profit_price": 52000.00,
  "status": "open",
  "opened_at": "2024-01-01T00:00:00Z"
}
```

### GET /api/v1/trading/positions
List user's positions.

**Query Parameters**:
- `strategy_id` (optional): Filter by strategy
- `symbol` (optional): Filter by symbol
- `status` (optional): Filter by status

**Response** (200):
```json
{
  "positions": [
    {
      "id": "uuid",
      "strategy_id": "uuid",
      "symbol": "BTCUSDT",
      "side": "buy",
      "quantity": 0.01,
      "entry_price": 50000.00,
      "current_price": 51000.00,
      "unrealized_pnl": 100.00,
      "status": "open",
      "opened_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### POST /api/v1/trading/positions/{id}/close
Close an open position.

**Request**:
```json
{
  "quantity": 0.01,
  "price": 52000.00
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "status": "closed",
  "exit_price": 52000.00,
  "realized_pnl": 200.00,
  "closed_at": "2024-01-01T00:00:00Z"
}
```

## Market Data Service API

### GET /api/v1/market-data/candles
Get market candles.

**Query Parameters**:
- `symbol` (required): Trading symbol
- `timeframe` (required): Candle timeframe
- `start` (optional): Start timestamp
- `end` (optional): End timestamp
- `limit` (default: 100): Max candles

**Response** (200):
```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "candles": [
    {
      "timestamp": "2024-01-01T00:00:00Z",
      "open": 50000.00,
      "high": 50500.00,
      "low": 49800.00,
      "close": 50200.00,
      "volume": 1234.56
    }
  ]
}
```

### GET /api/v1/market-data/tickers/{symbol}
Get current ticker for symbol.

**Response** (200):
```json
{
  "symbol": "BTCUSDT",
  "bid": 50100.00,
  "ask": 50101.00,
  "last": 50100.50,
  "volume_24h": 1234567.89,
  "price_change_24h": 1.5,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Portfolio Service API

### GET /api/v1/portfolio/value
Get current portfolio value.

**Response** (200):
```json
{
  "total_value": 12500.00,
  "available_balance": 500.00,
  "positions_value": 12000.00,
  "unrealized_pnl": 500.00,
  "realized_pnl_today": 150.00,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### GET /api/v1/portfolio/performance
Get strategy performance metrics.

**Response** (200):
```json
{
  "strategies": [
    {
      "id": "uuid",
      "name": "My Strategy",
      "total_trades": 150,
      "win_rate": 0.6,
      "avg_win": 150.00,
      "avg_loss": -75.00,
      "sharpe_ratio": 1.5,
      "max_drawdown": 0.15,
      "total_pnl": 2500.00
    }
  ]
}
```

## WebSocket API

### Connection
```
WebSocket: wss://api.quantx.ai/ws
Subprotocol: jwt
Authorization: Bearer <token>
```

### Channels Subscription
```json
{
  "action": "subscribe",
  "channels": ["positions:uuid", "predictions:uuid"]
}
```

### Position Update Message
```json
{
  "channel": "positions:uuid",
  "event": "position_updated",
  "data": {
    "id": "uuid",
    "status": "open",
    "current_price": 51000.00,
    "unrealized_pnl": 100.00,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### Prediction Message
```json
{
  "channel": "predictions:uuid",
  "event": "prediction_generated",
  "data": {
    "strategy_id": "uuid",
    "symbol": "BTCUSDT",
    "predicted_price": 52000.00,
    "confidence": 0.75,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## API Versioning

### URL Versioning
```
/api/v1/strategies
/api/v2/strategies  # Future
```

### Header Versioning
```
Accept: application/vnd.quantx.v1+json
Accept: application/vnd.quantx.v2+json
```

### Deprecation Policy
- 6 months notice before deprecation
- Version maintained for 12 months after deprecation
- Migration guide provided

## Pagination

### Cursor-based Pagination
```
GET /api/v1/orders?cursor=abc123&limit=50
```

Response:
```json
{
  "data": [...],
  "next_cursor": "def456",
  "has_more": true
}
```

## Filtering and Sorting

### Common Query Parameters
- `status`: Enum filter
- `created_after`: ISO timestamp
- `created_before`: ISO timestamp
- `sort`: Field name with optional direction
- `limit`: Page size (default 50, max 100)

## Related Documents
- [12_API_CONTRACTS.md](12_API_CONTRACTS.md)
- [02_SYSTEM_ARCHITECTURE.md](02_SYSTEM_ARCHITECTURE.md)
- [27_CONFIGURATION.md](27_CONFIGURATION.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: API Layer*