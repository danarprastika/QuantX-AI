# QuantX AI - Database Design

## Overview

This document defines the database architecture for QuantX AI, including database selection rationale, data partitioning strategy, connection management, and performance optimization approaches.

## Database Architecture Overview

QuantX AI uses a polyglot persistence approach with multiple databases optimized for specific query patterns:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Database Architecture                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
│   │   Layers     │  │   Layers     │  │   Layers     │  │   Layers     │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼─────────────────────────────────────────────────────────────┐    │
│   │                    Database Abstraction Layer                      │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │    │
│   │  │ Repository│  │ Repository│  │ Repository│  │ Repository│         │    │
│   │  │ Pattern   │  │ Pattern   │  │ Pattern   │  │ Pattern   │         │    │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Primary    │  │   Time       │  │   Document   │  │   Object     │
│  │   (PostgreSQL)│ │ (TimescaleDB)│ │   (MongoDB)  │ │   (S3)       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Database Selection Rationale

### PostgreSQL 16 (Primary Database)
- **Purpose**: Core business entities (Users, Strategies, Positions, Orders)
- **Rationale**: Strong consistency, JSONB support, mature ecosystem
- **ACID**: Full transaction support required for trading operations
- **Relationships**: Complex relationships between entities

### TimescaleDB 2.14
- **Purpose**: Time-series market data (candles, tickers, order books)
- **Rationale**: Automatic partitioning, compression, SQL interface
- **Benefits**: 90% compression ratio, faster time-based queries
- **Retention**: Automatic data retention policies

### MongoDB 7.0 (Document Database)
- **Purpose**: Event store, audit trail, session state
- **Rationale**: Flexible schema, horizontal scaling, high write throughput
- **Use Cases**: Event sourcing, conversation state, logs

### S3 Compatible Storage
- **Purpose**: Long-term archival, ML model storage
- **Rationale**: Cost-effective, durable, versioning support
- **Retention**: 7-year archival for compliance

## Data Partitioning Strategy

### PostgreSQL Partitioning

#### Time-based Partitioning
```sql
-- Positions partitioned by quarter
CREATE TABLE positions (
    id UUID PRIMARY KEY,
    strategy_id UUID NOT NULL,
    opened_at TIMESTAMP NOT NULL,
    ...
) PARTITION BY RANGE (opened_at);

CREATE TABLE positions_q1_2024 PARTITION OF positions
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE positions_q2_2024 PARTITION OF positions
FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
```

#### User-based Partitioning
```sql
-- Large users get dedicated partitions
CREATE TABLE positions_enterprise PARTITION OF positions
FOR VALUES IN ('enterprise_user_ids');
```

### TimescaleDB Partitioning

#### Automatic Time Partitioning
```sql
SELECT create_hypertable(
    'market_candles', 
    'timestamp',
    chunk_time_interval => INTERVAL '1 day'
);

-- Compression policy
ALTER TABLE market_candles SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',
    timescaledb.compress_orderby = 'timestamp DESC'
);
```

### MongoDB Sharding

#### Shard Key Selection
- Events: `{ "user_id": 1, "timestamp": 1 }` - User-time based
- Sessions: `{ "telegram_id": 1 }` - User-based

#### Index Strategy
```javascript
db.events.createIndex({ "user_id": 1, "timestamp": -1 })
db.events.createIndex({ "event_type": 1, "timestamp": 1 })
db.events.createIndex({ "correlation_id": 1 })
```

## Connection Management

### Connection Pool Configuration
| Database | Min Pool | Max Pool | Timeout | Connection TTL |
|----------|----------|----------|---------|----------------|
| PostgreSQL | 20 | 100 | 30s | 1h |
| TimescaleDB | 10 | 50 | 30s | 1h |
| MongoDB | 20 | 100 | 10s | 30m |
| Redis | 10 | 50 | 5s | N/A |

### Pool Implementation
```python
# infrastructure/database/pool.py
class ConnectionPool:
    def __init__(self) -> None:
        self.pools: dict[str, ConnectionPool] = {}
    
    async def get_pool(self, db_name: str) -> ConnectionPool:
        if db_name not in self.pools:
            self.pools[db_name] = await self._create_pool(db_name)
        return self.pools[db_name]
    
    def _create_pool(self, db_name: str) -> ConnectionPool:
        config = self._get_config(db_name)
        return asyncpg.create_pool(
            dsn=config.url,
            min_size=config.min_pool,
            max_size=config.max_pool,
            command_timeout=config.timeout,
        )
```

## Transaction Management

### Transaction Boundaries
- Strategy creation: Single transaction
- Order placement: Distributed transaction (outbox pattern)
- Position closure: Transaction with event outbox

### Outbox Pattern
```sql
-- Each service has an outbox table
CREATE TABLE strategy_outbox (
    id UUID PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    processed BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_strategy_outbox_unprocessed 
ON strategy_outbox (created_at) 
WHERE NOT processed;
```

### Two-Phase Commit Simulation
```python
# For cross-database consistency
class DistributedTransaction:
    async def __aenter__(self) -> 'DistributedTransaction':
        self.postgres_tx = await postgres_pool.begin()
        self.mongo_session = await mongo_client.start_session()
        return self
    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type:
            await self.postgres_tx.rollback()
            await self.mongo_session.abort_transaction()
        else:
            await self.postgres_tx.commit()
            await self.mongo_session.commit_transaction()
```

## Performance Optimization

### Indexing Strategy

#### Primary Database Indexes
```sql
-- Users table
CREATE INDEX idx_users_email ON users (email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_telegram ON users (telegram_id) WHERE deleted_at IS NULL;

-- Strategies table
CREATE INDEX idx_strategies_user ON strategies (user_id, status);
CREATE INDEX idx_strategies_symbol ON strategies (symbol) WHERE status = 'active';

-- Positions table
CREATE INDEX idx_positions_strategy ON positions (strategy_id, status);
CREATE INDEX idx_positions_symbol_time ON positions (symbol, opened_at DESC);

-- Orders table
CREATE INDEX idx_orders_position ON orders (position_id);
CREATE INDEX idx_orders_exchange ON orders (exchange_order_id);
CREATE INDEX idx_orders_status ON orders (status) WHERE status IN ('pending', 'submitted');
```

#### TimescaleDB Indexes
```sql
-- Candles
CREATE INDEX idx_candles_symbol_time ON market_candles (symbol, timestamp DESC);

-- Tickers
CREATE INDEX idx_tickers_symbol_time ON market_tickers (symbol, timestamp DESC);
CREATE INDEX idx_tickers_price_change ON market_tickers ((price - open_price));
```

### Query Optimization

#### Common Query Patterns
```sql
-- Get active strategies for user
SELECT * FROM strategies 
WHERE user_id = $1 AND status = 'active'
ORDER BY created_at DESC
LIMIT 50;

-- Get open positions with P&L
SELECT p.*, 
       (p.quantity * (t.last_price - p.entry_price)) as unrealized_pnl
FROM positions p
JOIN (
    SELECT symbol, last_price 
    FROM latest_prices
) t ON p.symbol = t.symbol
WHERE p.status = 'open' AND p.user_id = $1;
```

### Materialized Views
```sql
-- Daily portfolio performance
CREATE MATERIALIZED VIEW portfolio_daily_pnl AS
SELECT 
    user_id,
    date_trunc('day', created_at) as day,
    SUM(pnl) as daily_pnl
FROM position_closed_events
GROUP BY user_id, date_trunc('day', created_at);

CREATE UNIQUE INDEX idx_portfolio_daily_pnl 
ON portfolio_daily_pnl (user_id, day);

REFRESH MATERIALIZED VIEW CONCURRENTLY portfolio_daily_pnl;
```

## Backup and Recovery

### Backup Schedule
| Database | Full Backup | Incremental | Retention |
|----------|-------------|-------------|-----------|
| PostgreSQL | Daily 02:00 UTC | Hourly WAL | 30 days |
| TimescaleDB | Weekly | Daily | 90 days |
| MongoDB | Daily 03:00 UTC | Every 6h | 30 days |

### Point-in-Time Recovery
- PostgreSQL: Using WAL-G
- MongoDB: Oplog-based recovery
- TimescaleDB: Built-in point-in-time recovery

## Security

### Encryption at Rest
- PostgreSQL: TDE via pgcrypto extension
- TimescaleDB: Native encryption support
- MongoDB: Encrypted storage engine
- S3: SSE-S3 or SSE-KMS

### Access Control
```sql
-- Role-based access
CREATE ROLE quantx_app LOGIN;
GRANT CONNECT ON DATABASE quantx TO quantx_app;
GRANT USAGE ON SCHEMA trading TO quantx_app;
GRANT SELECT, INSERT, UPDATE ON positions TO quantx_app;
GRANT SELECT, INSERT, UPDATE ON strategies TO quantx_app;
REVOKE DELETE ON positions FROM quantx_app;
```

### Row-Level Security (RLS)
```sql
-- Users can only see their own data
ALTER TABLE positions ENABLE ROW LEVEL SECURITY;

CREATE POLICY position_isolation_policy 
ON positions FOR ALL 
USING (user_id = current_setting('app.current_user_id')::uuid);
```

## Monitoring

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Connection Count | Active DB connections | >80% pool |
| Query Duration | 95th percentile query time | >1s |
| Transaction Time | Average transaction duration | >5s |
| Replication Lag | Master-slave lag | >5s |
| Slow Queries | Queries >10s | Any |

### Query Analysis
```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

## Related Documents
- [05_DOMAIN_MODEL.md](05_DOMAIN_MODEL.md)
- [09_DATABASE_SCHEMA.md](09_DATABASE_SCHEMA.md)
- [10_ENTITY_RELATIONSHIP.md](10_ENTITY_RELATIONSHIP.md)
- [48_BACKUP_AND_RECOVERY.md](48_BACKUP_AND_RECOVERY.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Data Layer*