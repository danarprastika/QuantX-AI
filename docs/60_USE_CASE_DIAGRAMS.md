# QuantX AI - Use Case Diagrams

## Overview

This document provides use case diagrams for QuantX AI.

### Primary Use Cases

```
actor User
actor Telegram Bot
actor Exchange

User --> (Create Strategy)
User --> (View Positions)
User --> (View Performance)
User --> (Manage Settings)

Telegram Bot --> (Execute Strategy Commands)
Telegram Bot --> (Receive Notifications)

(Place Order) --> Exchange
(Place Order) <-- Exchange : Confirmations
```

## Related Documents
- [01_PROJECT_OVERVIEW.md](01_PROJECT_OVERVIEW.md)
- [56_SEQUENCE_DIAGRAMS.md](56_SEQUENCE_DIAGRAMS.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Process & Visualization*