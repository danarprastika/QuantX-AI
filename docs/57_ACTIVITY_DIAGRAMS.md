# QuantX AI - Activity Diagrams

## Overview

This document provides activity diagrams for QuantX AI workflows.

### Strategy Lifecycle Activity

```
title Strategy Lifecycle

start
:Strategy Created;
if (Activation requested?) then
  :Validate subscription;
  :Check risk limits;
endif
while (Active)
  :Receive market data;
  :Generate prediction;
  if (Confidence threshold met?) then
    :Place order;
  endif
  :Sleep until next interval;
endwhile
stop
```

## Related Documents
- [56_SEQUENCE_DIAGRAMS.md](56_SEQUENCE_DIAGRAMS.md)
- [58_COMPONENT_DIAGRAMS.md](58_COMPONENT_DIAGRAMS.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Process & Visualization*