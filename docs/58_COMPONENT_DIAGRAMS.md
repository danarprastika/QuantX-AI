---
status: Approved
owner: Architecture Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/58_COMPONENT_DIAGRAMS.md
depends_on:
  - docs/02_SYSTEM_ARCHITECTURE.md
  - docs/07_SERVICE_BOUNDARIES.md
related_documents:
  - docs/02_SYSTEM_ARCHITECTURE.md
  - docs/07_SERVICE_BOUNDARIES.md
---
# QuantX AI - Component Diagrams

## Overview

This document provides component diagrams for QuantX AI services and their interactions.

## Component Architecture

```
component TradingComponent {
  [Trading Service] as Trading
  [Position Repo] as PositionRepo
  [Order Repo] as OrderRepo
  [Exchange Adapter] as Exchange
  
  Trading --> PositionRepo: Save/Load
  Trading --> OrderRepo: Save/Load
  Trading --> Exchange: API Calls
}

component StrategyComponent {
  [Strategy Service] as Strategy
  [Strategy Repo] as StrategyRepo
  [AI Models] as Models
  [Prediction Service] as Prediction
  
  Strategy --> StrategyRepo: Save/Load
  Strategy --> Models: Train/Predict
  Strategy --> Prediction: Generate
}

TradingService --> StrategyService: Consume events
StrategyService --> TradingService: Emit events
```

## Related Documents
- [02_SYSTEM_ARCHITECTURE.md](02_SYSTEM_ARCHITECTURE.md)
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Architecture Team*
*Source of Truth: docs/58_COMPONENT_DIAGRAMS.md*
*Depends On: 02_SYSTEM_ARCHITECTURE.md, 07_SERVICE_BOUNDARIES.md*
*Related Documents: 02_SYSTEM_ARCHITECTURE.md, 07_SERVICE_BOUNDARIES.md*
*Phase: Process & Visualization*
