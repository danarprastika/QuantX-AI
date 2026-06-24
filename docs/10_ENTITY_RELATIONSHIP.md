# QuantX AI - Entity Relationship

## Overview

This document describes the entity relationships, cardinality, and business rules governing data interactions in QuantX AI. The relationships are defined across the polyglot database architecture.

## Entity Relationship Diagram

```
                    ┌────────────────────┐
                    │       USERS        │
                    └──────────┬─────────┘
                               │ 1
                               │
                    ┌──────────▼─────────┐
                    │    STRATEGIES      │
                    └──────────┬─────────┘
                               │ 1
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         │ 1                   │ 1..*               │
         │                     │                     │
┌────────▼──────────┐   ┌──────▼───────┐   ┌─────────▼─────────┐
│    POSITIONS      │   │     ORDERS   │   │   PREDICTIONS     │
└───────────────────┘   └──────────────┘   └───────────────────┘

┌───────────────────┐
│   MARKET_DATA     │
│  (TimescaleDB)    │
└───────────────────┘
```

## Detailed Relationships

### User to Strategy (One-to-Many)
```
User 1 ──► Strategy 1..*
```

**Cardinality**: One user can have zero to many strategies

**Business Rules**:
1. User must exist before strategy creation
2. Deleting user cascades to strategies
3. Strategy count limited by subscription tier
4. User email must be unique across system

**SQL FK**:
```sql
ALTER TABLE strategies 
ADD CONSTRAINT fk_strategy_user 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

### Strategy to Position (One-to-Many)
```
Strategy 1 ──► Position 1..*
```

**Cardinality**: One strategy can have zero to many positions over its lifetime

**Business Rules**:
1. Only ACTIVE strategies create positions
2. Position symbol must match strategy symbol
3. Strategy cannot be deleted while positions exist
4. Position count affects strategy status

**SQL FK**:
```sql
ALTER TABLE positions 
ADD CONSTRAINT fk_position_strategy 
FOREIGN KEY (strategy_id) REFERENCES strategies(id);
```

### Strategy to Prediction (One-to-Many)
```
Strategy 1 ──► Prediction 1..*
```

**Cardinality**: One strategy generates zero to many predictions

**Business Rules**:
1. Prediction timeframe matches strategy timeframe
2. Prediction symbol matches strategy symbol
3. Confidence score required for trading signals
4. Predictions expire after time window

**SQL FK**:
```sql
ALTER TABLE predictions 
ADD CONSTRAINT fk_prediction_strategy 
FOREIGN KEY (strategy_id) REFERENCES strategies(id);
```

### Position to Order (One-to-Many)
```
Position 1 ──► Order 1..*
```

**Cardinality**: One position has exactly one order initially, may have additional for modifications

**Business Rules**:
1. Opening position creates primary order
2. Closing position creates closing order
3. Order status must be FILLED before position closure
4. Order quantity must equal position quantity

**SQL FK**:
```sql
ALTER TABLE orders 
ADD CONSTRAINT fk_order_position 
FOREIGN KEY (position_id) REFERENCES positions(id);
```

### Position to Strategy (Many-to-One)
```
Position * ──► Strategy 1
```

**Cardinality**: Many positions reference one strategy

**Business Rules**:
1. Position inherits symbol from strategy
2. Position inherits risk parameters from strategy config
3. Strategy status changes affect position behavior

### User to Position (One-to-Many via Strategy)
```
User 1 ──► Strategy 1..* ──► Position 1..*
```

**Cardinality**: Transitive through strategy

**Business Rules**:
1. User owns all positions of their strategies
2. User P&L calculated from all positions
3. Risk limits applied at user level

**SQL FK**:
```sql
ALTER TABLE positions 
ADD CONSTRAINT fk_position_user 
FOREIGN KEY (user_id) REFERENCES users(id);
```

## Market Data Relationships (TimescaleDB)

### Symbol to Candles (One-to-Many)
```
Symbol 1 ──► Candle {timeframe} 1..*
```

**Cardinality**: Infinite historical candles per symbol/timeframe combination

**Business Rules**:
1. Candles ordered by timestamp
2. No gaps in candle sequence
3. Duplicate timestamps rejected

### Candle to Ticker (One-to-Many)
```
Candle time ──► Ticker updates (within timeframe)
```

**Cardinality**: Many tickers per candle period

**Business Rules**:
1. Tickers aggregate into candles
2. OHLC derived from tickers
3. Volume sums tickers

## Event Store Relationships (MongoDB)

### Aggregate to Events (One-to-Many)
```
Aggregate 1 ──► Event 1..*
```

**Cardinality**: Infinite events per aggregate

**Business Rules**:
1. Events ordered by timestamp
2. Event versions monotonically increasing
3. Correlation ID links related events

### User to Events (One-to-Many)
```
User 1 ──► Event (via aggregate) 1..*
```

**Cardinality**: All user-related events

**Business Rules**:
1. User ID in event metadata
2. Events partitioned by user for queries
3. Audit trail completeness

## Subscription Relationships

### User to Subscription (One-to-One)
```
User 1 ──► Subscription 0..1 (Historical) 1 (Current)
```

**Cardinality**: One current subscription per user

**Business Rules**:
1. Subscription required for trading
2. Tier limits strategy count and features
3. Expiration triggers grace period

## Risk Management Relationships

### User to Risk Limits (One-to-Many)
```
User 1 ──► RiskLimit 1..* (by symbol)
```

**Cardinality**: Multiple risk limits per user

**Business Rules**:
1. Total exposure limit across symbols
2. Position count limit per symbol
3. Daily loss limit across all strategies

## Cross-Database Relationships

### Strategy ID Consistency
All databases use the same UUID for strategy IDs:
- PostgreSQL: Primary source of truth
- MongoDB: References same UUID
- TimescaleDB: References via tags

### Event Correlation
Events reference entities across databases:
```json
{
  "aggregate_id": "strategy-uuid",
  "aggregate_type": "strategy",
  "payload": {
    "position_id": "position-uuid",
    "user_id": "user-uuid"
  }
}
```

## Entity Lifecycle Dependencies

### User Lifecycle
```
Created → Active → (Subscription Expired) → Grace Period → Inactive
                                          ↘ Cancelled
```

### Strategy Lifecycle
```
Draft → Active → (Positions Open) → Paused → Stopped → Archived
                      ↓
                 [Position created]
```

### Position Lifecycle
```
Created → Open → (Order Filled) → Closed
           ↓ Cancel
       Cancelled
```

### Order Lifecycle
```
Created → Submitted → Partially Filled → Filled
                    ↓
                 Cancelled/Rejected
```

## Cascade Rules

| Table | Delete Action | Reason |
|-------|---------------|--------|
| Strategies | CASCADE | User deletion removes all strategies |
| Positions | CASCADE | Strategy deletion removes positions |
| Orders | CASCADE | Position deletion removes orders |
| Events | NONE | Historical record retention |
| Sessions | CASCADE | User deletion clears sessions |

## Aggregate Boundaries

### Strategy Aggregate
- Strategy (root)
- Position (child entities)
- Order (child entities)
- Prediction (child entities when created)

**Invariant**: Only strategy root can be retrieved in isolation

### Position Aggregate
- Position (root)
- Order (child entities)

**Invariant**: Position state determines valid order operations

## Related Documents
- [05_DOMAIN_MODEL.md](05_DOMAIN_MODEL.md)
- [08_DATABASE_DESIGN.md](08_DATABASE_DESIGN.md)
- [09_DATABASE_SCHEMA.md](09_DATABASE_SCHEMA.md)
- [32_ERROR_HANDLING.md](32_ERROR_HANDLING.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Data Layer*