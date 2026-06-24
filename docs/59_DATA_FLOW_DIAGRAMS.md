---
status: Approved
owner: Architecture Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/59_DATA_FLOW_DIAGRAMS.md
depends_on:
  - docs/02_SYSTEM_ARCHITECTURE.md
  - docs/58_COMPONENT_DIAGRAMS.md
related_documents:
  - docs/02_SYSTEM_ARCHITECTURE.md
  - docs/58_COMPONENT_DIAGRAMS.md
---
# QuantX AI - Data Flow Diagrams

## Overview

This document provides data flow diagrams for QuantX AI.

### Core Data Flow

```
title Core Data Flow

Market Data Sources -> Market Data Service: WebSocket/REST
Market Data Service -> TimescaleDB: Store candles
Market Data Service -> Event Bus: Publish market events
Strategy Service -> TimescaleDB: Query historical data
Strategy Service -> AI Models: Generate predictions
AI Models -> Strategy Service: Predictions
Strategy Service -> Event Bus: Publish prediction events
Event Bus -> Trading Service: Prediction events
Trading Service -> Exchange API: Place orders
Exchange API -> Trading Service: Order confirmations
Trading Service -> PostgreSQL: Update positions
Trading Service -> Event Bus: Publish trade events
Event Bus -> Telegram Service: Notify user
Telegram Service -> User: Send message
```

## Related Documents
- [02_SYSTEM_ARCHITECTURE.md](02_SYSTEM_ARCHITECTURE.md)
- [58_COMPONENT_DIAGRAMS.md](58_COMPONENT_DIAGRAMS.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Architecture Team*
*Source of Truth: docs/59_DATA_FLOW_DIAGRAMS.md*
*Depends On: 02_SYSTEM_ARCHITECTURE.md, 58_COMPONENT_DIAGRAMS.md*
*Related Documents: 02_SYSTEM_ARCHITECTURE.md, 58_COMPONENT_DIAGRAMS.md*
*Phase: Process & Visualization*
