---
status: Approved
owner: Architecture Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/56_SEQUENCE_DIAGRAMS.md
depends_on:
  - docs/57_ACTIVITY_DIAGRAMS.md
  - docs/58_COMPONENT_DIAGRAMS.md
related_documents:
  - docs/57_ACTIVITY_DIAGRAMS.md
  - docs/58_COMPONENT_DIAGRAMS.md
---
# QuantX AI - Sequence Diagrams

## Overview

This document provides sequence diagrams for key workflows in QuantX AI.

### Strategy Creation Sequence

```
title Strategy Creation Workflow

User->Telegram Service: /create_strategy
Telegram Service->User Service: Validate user
User Service-->Telegram Service: User OK
Telegram Service->Strategy Service: CreateStrategyCommand
Strategy Service->Database: Save strategy
Database-->Strategy Service: Strategy ID
Strategy Service->Event Bus: Publish StrategyCreated
Event Bus->Trading Service: StrategyCreated event
Trading Service-->Event Bus: Ack
Telegram Service->Telegram Service: Send confirmation
Telegram Service->User: "Strategy created"
```

### Order Execution Sequence

```
title Order Execution Workflow

Market Data->Strategy Service: New candle
Strategy Service->AI Model: Generate prediction
AI Model-->Strategy Service: Prediction
Strategy Service->Event Bus: Publish PredictionGenerated
Event Bus->Trading Service: PredictionGenerated
Trading Service->Risk Engine: Validate trade
Risk Engine-->Trading Service: Approved/Denied
alt If Approved
    Trading Service->Exchange API: Place order
    Exchange API-->Trading Service: Order ID
    Trading Service->Database: Save order
    Trading Service->Event Bus: Publish OrderSubmitted
end
```

## Related Documents
- [57_ACTIVITY_DIAGRAMS.md](57_ACTIVITY_DIAGRAMS.md)
- [58_COMPONENT_DIAGRAMS.md](58_COMPONENT_DIAGRAMS.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Architecture Team*
*Source of Truth: docs/56_SEQUENCE_DIAGRAMS.md*
*Depends On: 57_ACTIVITY_DIAGRAMS.md, 58_COMPONENT_DIAGRAMS.md*
*Related Documents: 57_ACTIVITY_DIAGRAMS.md, 58_COMPONENT_DIAGRAMS.md*
*Phase: Process & Visualization*
