# QuantX AI - Database Schema

## Overview

This document defines the complete database schema for QuantX AI, including table definitions, constraints, indexes, and partitioning strategy. Each schema is designed for its specific database technology.

## PostgreSQL Schema (Primary Database)

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_id BIGINT UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    subscription_tier subscription_tier NOT NULL DEFAULT 'free',
    subscription_expires TIMESTAMP WITH TIME ZONE,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT chk_subscription_dates 
        CHECK (subscription_expires IS NULL OR subscription_expires > created_at)
);

CREATE INDEX idx_users_email ON users (email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_telegram ON users (telegram_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_subscription ON users (subscription_tier, subscription_expires);
```

### Strategies Table
```sql
CREATE TYPE strategy_status AS ENUM (
    'draft', 'active', 'paused', 'stopped', 'archived'
);

CREATE TYPE strategy_type AS ENUM (
    'lstm_prediction', 'transformer', 'ensemble', 
    'rsi_momentum', 'moving_average'
);

CREATE TABLE strategies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    type strategy_type NOT NULL,
    config JSONB NOT NULL,
    status strategy_status NOT NULL DEFAULT 'draft',
    model_version VARCHAR(50),
    performance_score DECIMAL(5,4),
    last_prediction_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    CONSTRAINT chk_strategy_config CHECK (jsonb_typeof(config) = 'object')
);

CREATE INDEX idx_strategies_user ON strategies (user_id, status);
CREATE INDEX idx_strategies_symbol ON strategies (symbol) WHERE status = 'active';
CREATE INDEX idx_strategies_type ON strategies (type);
```

### Positions Table
```sql
CREATE TYPE position_side AS ENUM ('buy', 'sell');
CREATE TYPE position_status AS ENUM ('open', 'closed', 'cancelled');

CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_id UUID NOT NULL REFERENCES strategies(id),
    user_id UUID NOT NULL REFERENCES users(id),
    symbol VARCHAR(20) NOT NULL,
    side position_side NOT NULL,
    quantity DECIMAL(20,8) NOT NULL CHECK (quantity > 0),
    entry_price DECIMAL(20,8) NOT NULL CHECK (entry_price > 0),
    exit_price DECIMAL(20,8) CHECK (exit_price > 0),
    stop_loss_price DECIMAL(20,8) CHECK (stop_loss_price > 0),
    take_profit_price DECIMAL(20,8) CHECK (take_profit_price > 0),
    status position_status NOT NULL DEFAULT 'open',
    exchange_order_id VARCHAR(100),
    opened_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    CONSTRAINT chk_exit_requires_status 
        CHECK (closed_at IS NULL OR status = 'closed'),
    CONSTRAINT chk_exit_price_required 
        CHECK (status != 'closed' OR exit_price IS NOT NULL)
);

-- Partitioning setup would be applied here
CREATE INDEX idx_positions_strategy ON positions (strategy_id, status);
CREATE INDEX idx_positions_user ON positions (user_id, status);
CREATE INDEX idx_positions_symbol ON positions (symbol, status);
```

### Orders Table
```sql
CREATE TYPE order_type AS ENUM ('market', 'limit', 'stop', 'stop_limit');
CREATE TYPE order_status AS ENUM (
    'pending', 'submitted', 'partially_filled', 
    'filled', 'cancelled', 'rejected'
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    position_id UUID NOT NULL REFERENCES positions(id),
    user_id UUID NOT NULL REFERENCES users(id),
    exchange_order_id VARCHAR(100) UNIQUE,
    symbol VARCHAR(20) NOT NULL,
    side position_side NOT NULL,
    type order_type NOT NULL,
    quantity DECIMAL(20,8) NOT NULL CHECK (quantity > 0),
    price DECIMAL(20,8) CHECK (price > 0),
    status order_status NOT NULL DEFAULT 'pending',
    executed_quantity DECIMAL(20,8) DEFAULT 0,
    average_price DECIMAL(20,8),
    exchange_response JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    CONSTRAINT chk_price_required 
        CHECK (type = 'market' OR price IS NOT NULL),
    CONSTRAINT chk_executed_not_exceeds 
        CHECK (executed_quantity <= quantity)
);

CREATE INDEX idx_orders_position ON orders (position_id);
CREATE INDEX idx_orders_exchange ON orders (exchange_order_id);
CREATE INDEX idx_orders_status ON orders (status) 
    WHERE status IN ('pending', 'submitted');
CREATE INDEX idx_orders_user ON orders (user_id, created_at DESC);
```

## TimescaleDB Schema (Market Data)

### Market Candles Table
```sql
CREATE TABLE market_candles (
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    open_price DECIMAL(20,8) NOT NULL,
    high_price DECIMAL(20,8) NOT NULL,
    low_price DECIMAL(20,8) NOT NULL,
    close_price DECIMAL(20,8) NOT NULL,
    volume DECIMAL(20,8) NOT NULL,
    trades INTEGER,
    
    PRIMARY KEY (symbol, timeframe, timestamp)
);

SELECT create_hypertable(
    'market_candles', 
    'timestamp',
    chunk_time_interval => INTERVAL '1 day'
);

-- Indexes
CREATE INDEX idx_candles_symbol_time ON market_candles (symbol, timestamp DESC);
CREATE INDEX idx_candles_time_range ON market_candles (timeframe, timestamp);
```

### Market Tickers Table
```sql
CREATE TABLE market_tickers (
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    bid_price DECIMAL(20,8) NOT NULL,
    ask_price DECIMAL(20,8) NOT NULL,
    last_price DECIMAL(20,8) NOT NULL,
    volume_24h DECIMAL(20,8),
    price_change_24h DECIMAL(20,8),
    
    PRIMARY KEY (symbol, timestamp)
);

SELECT create_hypertable(
    'market_tickers', 
    'timestamp',
    chunk_time_interval => INTERVAL '1 hour'
);

CREATE INDEX idx_tickers_symbol_time ON market_tickers (symbol, timestamp DESC);
```

### Order Books Table
```sql
CREATE TABLE order_books (
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    side VARCHAR(4) NOT NULL, -- 'bid' or 'ask'
    price DECIMAL(20,8) NOT NULL,
    quantity DECIMAL(20,8) NOT NULL,
    
    PRIMARY KEY (symbol, timestamp, side, price)
);

SELECT create_hypertable(
    'order_books', 
    'timestamp',
    chunk_time_interval => INTERVAL '1 hour'
);
```

## MongoDB Schema (Document/Event Store)

### Events Collection
```javascript
// events collection
{
  "_id": ObjectId(),
  "event_id": UUID,
  "correlation_id": UUID,
  "event_type": "string",  // e.g., "PositionOpened", "OrderFilled"
  "aggregate_id": UUID,
  "aggregate_type": "string", // e.g., "position", "order", "strategy"
  "payload": {},  // Event data
  "timestamp": ISODate,
  "version": 1,
  "metadata": {
    "user_id": UUID,
    "source_ip": "string",
    "user_agent": "string"
  }
}

// Indexes
db.events.createIndex({ "event_type": 1, "timestamp": -1 })
db.events.createIndex({ "aggregate_id": 1, "aggregate_type": 1 })
db.events.createIndex({ "correlation_id": 1 })
db.events.createIndex({ "timestamp": 1 }, { "expireAfterSeconds": 2592000 }) // 30 days
```

### Sessions Collection
```javascript
// sessions collection
{
  "_id": ObjectId(),
  "telegram_id": "bigint",
  "user_id": UUID,
  "state": {},  // FSM context
  "last_activity": ISODate,
  "created_at": ISODate
}

// Indexes
db.sessions.createIndex({ "telegram_id": 1 }, { "unique": true })
db.sessions.createIndex({ "last_activity": 1 }, { "expireAfterSeconds": 86400 }) // 24h
```

## Redis Schema (Cache/Session)

### Cache Keys
```
# Market data cache
market:{symbol}:{timeframe} -> MarketData JSON, TTL 60s

# User session cache
session:{telegram_id} -> Session JSON, TTL 24h

# Rate limit counters
rate_limit:{user_id}:{endpoint} -> count, TTL 1m

# Position cache
position:{strategy_id}:{symbol} -> Position JSON, TTL 5m
```

### Pub/Sub Channels
```
# Prediction broadcasts
predictions:{symbol} -> Prediction messages

# Order status updates
order_updates:{user_id} -> Order status messages

# System notifications
notifications:{user_id} -> Notification messages
```

## Tablespaces and Storage

### PostgreSQL Tablespaces
```sql
-- Tablespace for primary data
CREATE TABLESPACE quantx_data 
LOCATION '/var/lib/postgresql/data';

-- Tablespace for indexes
CREATE TABLESPACE quantx_indexes 
LOCATION '/var/lib/postgresql/indexes';

-- Tablespace for WAL
CREATE TABLESPACE quantx_wal 
LOCATION '/var/lib/postgresql/wal';
```

### TimescaleDB Retention
```sql
-- Compress data after 7 days
SELECT add_compression_policy(
    'market_candles', 
    INTERVAL '7 days'
);

-- Drop data after 1 year
SELECT add_retention_policy(
    'market_candles', 
    INTERVAL '1 year'
);

-- Keep tickers for 30 days
SELECT add_retention_policy(
    'market_tickers', 
    INTERVAL '30 days'
);
```

## Constraints and Validation

### Check Constraints
```sql
-- Positive values check
ALTER TABLE positions 
ADD CONSTRAINT chk_positive_values 
CHECK (quantity > 0 AND entry_price > 0);

-- Date order check
ALTER TABLE positions 
ADD CONSTRAINT chk_date_order 
CHECK (closed_at IS NULL OR closed_at > opened_at);

-- Price logic check
ALTER TABLE positions 
ADD CONSTRAINT chk_stop_logic 
CHECK (
    (side = 'buy' AND stop_loss_price IS NULL OR stop_loss_price < entry_price) OR
    (side = 'sell' AND stop_loss_price IS NULL OR stop_loss_price > entry_price)
);
```

### FK Constraints
```sql
ALTER TABLE strategies 
ADD CONSTRAINT fk_strategy_user 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE positions 
ADD CONSTRAINT fk_position_strategy 
FOREIGN KEY (strategy_id) REFERENCES strategies(id) ON DELETE CASCADE;

ALTER TABLE positions 
ADD CONSTRAINT fk_position_user 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

## Views

### User Portfolio View
```sql
CREATE VIEW user_portfolio AS
SELECT 
    u.id as user_id,
    p.symbol,
    SUM(p.quantity * (COALESCE(p.exit_price, t.last_price) - p.entry_price)) as realized_pnl,
    SUM(CASE WHEN p.status = 'open' THEN p.quantity ELSE 0 END) as open_quantity
FROM users u
LEFT JOIN positions p ON u.id = p.user_id
LEFT JOIN latest_prices t ON p.symbol = t.symbol
GROUP BY u.id, p.symbol;
```

### Strategy Performance View
```sql
CREATE VIEW strategy_performance AS
SELECT 
    s.id,
    s.user_id,
    COUNT(o.id) FILTER (WHERE o.status = 'filled') as filled_orders,
    COUNT(o.id) FILTER (WHERE o.status = 'cancelled') as cancelled_orders,
    AVG(o.average_price * o.quantity) as avg_trade_value
FROM strategies s
LEFT JOIN positions p ON s.id = p.strategy_id
LEFT JOIN orders o ON p.id = o.position_id
GROUP BY s.id, s.user_id;
```

## Related Documents
- [08_DATABASE_DESIGN.md](08_DATABASE_DESIGN.md)
- [10_ENTITY_RELATIONSHIP.md](10_ENTITY_RELATIONSHIP.md)
- [05_DOMAIN_MODEL.md](05_DOMAIN_MODEL.md)
- [09_DATABASE_SCHEMA.md](09_DATABASE_SCHEMA.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Data Layer*