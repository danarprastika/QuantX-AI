---
status: Approved
owner: Backend Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/12_API_CONTRACTS.md
depends_on:
  - docs/11_API_SPECIFICATION.md
  - docs/26_EVENT_SYSTEM.md
  - docs/33_VALIDATION.md
related_documents:
  - docs/11_API_SPECIFICATION.md
  - docs/26_EVENT_SYSTEM.md
  - docs/33_VALIDATION.md
---
# QuantX AI - API Contracts

## Overview

This document defines the service-to-service contracts and API specifications in detail, including request/response schemas, data validation rules, and consumer contracts.

## Contract Principles

### Consumer-Driven Contracts
- Providers must fulfill contracts defined by consumers
- Contracts versioned independently
- Breaking changes require deprecation cycle
- Automated contract testing in CI/CD

### Idempotency
All write operations must be idempotent:
- Same request ID produces same result
- Duplicate requests return existing resource
- Safe retry mechanism

## Strategy Service Contracts

### StrategyCreated Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "StrategyCreated",
  "type": "object",
  "required": ["event_id", "strategy_id", "user_id", "timestamp"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid"
    },
    "strategy_id": {
      "type": "string",
      "format": "uuid"
    },
    "user_id": {
      "type": "string",
      "format": "uuid"
    },
    "strategy_type": {
      "type": "string",
      "enum": ["lstm_prediction", "transformer", "ensemble", "rsi_momentum", "moving_average"]
    },
    "symbol": {
      "type": "string",
      "pattern": "^[A-Z]{3,10}$"
    },
    "timeframe": {
      "type": "string",
      "enum": ["1m", "5m", "15m", "1h", "4h", "1d"]
    },
    "config": {
      "type": "object",
      "properties": {
        "risk_limit": {"type": "number", "minimum": 0},
        "stop_loss_pct": {"type": "number", "minimum": 0},
        "take_profit_pct": {"type": "number", "minimum": 0},
        "confidence_threshold": {"type": "number", "minimum": 0, "maximum": 1}
      },
      "required": ["risk_limit", "confidence_threshold"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    }
  }
}
```

### StrategyActivated Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "StrategyActivated",
  "type": "object",
  "required": ["event_id", "strategy_id", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "strategy_id": {"type": "string", "format": "uuid"},
    "activated_by": {"type": "string", "format": "uuid"},
    "activation_params": {
      "type": "object",
      "properties": {
        "max_positions": {"type": "integer", "minimum": 1},
        "daily_loss_limit": {"type": "number", "minimum": 0}
      }
    },
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

### PredictionGenerated Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PredictionGenerated",
  "type": "object",
  "required": ["event_id", "strategy_id", "symbol", "predicted_price", "confidence", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "strategy_id": {"type": "string", "format": "uuid"},
    "symbol": {"type": "string", "pattern": "^[A-Z]{3,10}$"},
    "predicted_price": {"type": "number", "minimum": 0},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "timeframe": {"type": "string", "enum": ["1m", "5m", "15m", "1h", "4h", "1d"]},
    "model_version": {"type": "string"},
    "features_used": {
      "type": "array",
      "items": {"type": "string"}
    },
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

## Trading Service Contracts

### PositionOpened Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PositionOpened",
  "type": "object",
  "required": ["event_id", "position_id", "strategy_id", "symbol", "side", "quantity", "entry_price", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "position_id": {"type": "string", "format": "uuid"},
    "strategy_id": {"type": "string", "format": "uuid"},
    "user_id": {"type": "string", "format": "uuid"},
    "symbol": {"type": "string", "pattern": "^[A-Z]{3,10}$"},
    "side": {"type": "string", "enum": ["buy", "sell"]},
    "quantity": {"type": "number", "minimum": 0},
    "entry_price": {"type": "number", "minimum": 0},
    "stop_loss_price": {"type": "number", "minimum": 0},
    "take_profit_price": {"type": "number", "minimum": 0},
    "exchange_order_id": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

### OrderSubmitted Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OrderSubmitted",
  "type": "object",
  "required": ["event_id", "order_id", "position_id", "symbol", "side", "quantity", "exchange_order_id", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "order_id": {"type": "string", "format": "uuid"},
    "position_id": {"type": "string", "format": "uuid"},
    "exchange_order_id": {"type": "string"},
    "symbol": {"type": "string", "pattern": "^[A-Z]{3,10}$"},
    "side": {"type": "string", "enum": ["buy", "sell"]},
    "type": {"type": "string", "enum": ["market", "limit", "stop", "stop_limit"]},
    "quantity": {"type": "number", "minimum": 0},
    "price": {"type": "number", "minimum": 0},
    "exchange": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

### OrderFilled Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OrderFilled",
  "type": "object",
  "required": ["event_id", "order_id", "position_id", "filled_quantity", "fill_price", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "order_id": {"type": "string", "format": "uuid"},
    "position_id": {"type": "string", "format": "uuid"},
    "strategy_id": {"type": "string", "format": "uuid"},
    "user_id": {"type": "string", "format": "uuid"},
    "filled_quantity": {"type": "number", "minimum": 0},
    "fill_price": {"type": "number", "minimum": 0},
    "fees": {"type": "number", "minimum": 0},
    "exchange": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

## Market Data Service Contracts

### MarketDataReceived Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MarketDataReceived",
  "type": "object",
  "required": ["event_id", "symbol", "event_type", "data", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "symbol": {"type": "string", "pattern": "^[A-Z]{3,10}$"},
    "event_type": {"type": "string", "enum": ["ticker", "candle", "orderbook"]},
    "exchange": {"type": "string", "enum": ["binance", "coinbase", "kraken", "ftx"]},
    "data": {
      "type": "object",
      "properties": {
        "bid": {"type": "number"},
        "ask": {"type": "number"},
        "last": {"type": "number"},
        "volume": {"type": "number"},
        "timestamp": {"type": "string", "format": "date-time"}
      }
    },
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

## User Auth Service Contracts

### UserRegistered Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UserRegistered",
  "type": "object",
  "required": ["event_id", "user_id", "telegram_id", "email", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "user_id": {"type": "string", "format": "uuid"},
    "telegram_id": {"type": "integer", "minimum": 0},
    "email": {"type": "string", "format": "email"},
    "initial_preferences": {"type": "object"},
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

### SubscriptionActivated Contract
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SubscriptionActivated",
  "type": "object",
  "required": ["event_id", "user_id", "tier", "expires_at", "timestamp"],
  "properties": {
    "event_id": {"type": "string", "format": "uuid"},
    "user_id": {"type": "string", "format": "uuid"},
    "tier": {"type": "string", "enum": ["free", "basic", "premium", "enterprise"]},
    "expires_at": {"type": "string", "format": "date-time"},
    "payment_id": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

## HTTP API Request Schemas

### StrategyCreateRequest
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "StrategyCreateRequest",
  "type": "object",
  "required": ["name", "symbol", "timeframe", "type", "config"],
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "symbol": {
      "type": "string",
      "pattern": "^[A-Z]{3,10}$"
    },
    "timeframe": {
      "type": "string",
      "enum": ["1m", "5m", "15m", "1h", "4h", "1d"]
    },
    "type": {
      "type": "string",
      "enum": ["lstm_prediction", "transformer", "ensemble", "rsi_momentum", "moving_average"]
    },
    "config": {
      "type": "object",
      "required": ["risk_limit", "confidence_threshold"],
      "properties": {
        "risk_limit": {"type": "number", "minimum": 0, "maximum": 100000},
        "stop_loss_pct": {"type": "number", "minimum": 0, "maximum": 100},
        "take_profit_pct": {"type": "number", "minimum": 0, "maximum": 100},
        "confidence_threshold": {"type": "number", "minimum": 0, "maximum": 1}
      }
    }
  }
}
```

### PositionCloseRequest
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PositionCloseRequest",
  "type": "object",
  "properties": {
    "quantity": {"type": "number", "minimum": 0},
    "price": {"type": "number", "minimum": 0}
  }
}
```

## HTTP API Response Schemas

### Error Response
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ErrorResponse",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": {
      "type": "object",
      "required": ["code", "message"],
      "properties": {
        "code": {"type": "string"},
        "message": {"type": "string"},
        "details": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "field": {"type": "string"},
              "error": {"type": "string"}
            }
          }
        },
        "correlation_id": {"type": "string", "format": "uuid"},
        "timestamp": {"type": "string", "format": "date-time"}
      }
    }
  }
}
```

### PaginatedResponse
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PaginatedResponse",
  "type": "object",
  "required": ["data", "total", "limit", "offset"],
  "properties": {
    "data": {"type": "array"},
    "total": {"type": "integer"},
    "limit": {"type": "integer"},
    "offset": {"type": "integer"},
    "next_cursor": {"type": "string"}
  }
}
```

## Validation Rules

### Symbol Validation
- 3-10 uppercase letters
- Must be in exchange whitelist
- Cannot contain numbers or special characters

### Quantity Validation
- Minimum: Exchange-specific
- Maximum: Account balance dependent
- Decimal precision: 8 places

### Price Validation
- Must be positive
- Must be within exchange tick size
- Stop loss must be valid for side

### Timeframe Validation
- Must be in supported list
- Strategy timeframe fixed after activation

## Correlation and Tracing

### Correlation ID Propagation
All requests carry `X-Correlation-ID` header:
- Generated if not present
- Propagated through all service calls
- Logged with every operation

### Event Tracing
```json
{
  "correlation_id": "uuid",
  "causation_id": "parent-uuid",
  "trace_id": "long-trace-uuid",
  "span_id": "short-span-uuid"
}
```

## Backward Compatibility

### Non-Breaking Changes
- Adding optional fields
- Adding new enum values
- Adding new endpoints
- Adding new event types

### Breaking Changes
- Removing fields
- Changing field types
- Removing enum values
- Changing validation rules

### Version Negotiation
Services negotiate compatible versions:
- Check `API-Version` header
- Fall back to supported versions
- Return error 426 for unsupported versions

## Consumer Contracts

### Trading Service Consumes
- `StrategyActivated` - Start monitoring for signals
- `StrategyPaused` - Stop signal evaluation
- `StrategyStopped` - Close all positions
- `PredictionGenerated` - Evaluate trading signal

### Strategy Service Consumes
- `OrderFilled` - Calculate strategy P&L
- `PositionClosed` - Finalize strategy metrics
- `UserUpdated` - Validate subscription status

## Related Documents
- [11_API_SPECIFICATION.md](11_API_SPECIFICATION.md)
- [26_EVENT_SYSTEM.md](26_EVENT_SYSTEM.md)
- [33_VALIDATION.md](33_VALIDATION.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Backend Team*
*Source of Truth: docs/12_API_CONTRACTS.md*
*Depends On: 11_API_SPECIFICATION.md, 26_EVENT_SYSTEM.md, 33_VALIDATION.md*
*Related Documents: 11_API_SPECIFICATION.md, 26_EVENT_SYSTEM.md, 33_VALIDATION.md*
*Phase: API Layer*
