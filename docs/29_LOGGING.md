---
status: Approved
owner: DevOps Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/29_LOGGING.md
depends_on:
  - docs/31_OBSERVABILITY.md
  - docs/29_LOGGING.md
  - docs/15_SECURITY.md
related_documents:
  - docs/31_OBSERVABILITY.md
  - docs/29_LOGGING.md
  - docs/15_SECURITY.md
---
# QuantX AI - Logging

## Overview

This document defines the logging architecture for QuantX AI, including log levels, formats, destinations, sampling, and compliance considerations.

## Logging Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Logging Pipeline                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │   Service    │  │   Service    │  │   Service    │                 │
│   │   Logger     │  │   Logger     │  │   Logger     │                 │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│          │                 │                 │                         │
│   ┌──────▼────────────────────────────────────────────────────────┐    │
│   │                    Loki Aggregation                            │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│   │  │ Strategy │  │ Trading  │  │ Market   │  │ User     │        │    │
│   │  │ Logs     │  │ Logs     │  │ Logs     │  │ Logs     │        │    │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Promtail   │  │   Promtail   │  │   Promtail   │  │   Promtail   │ │
│  │   Agent      │  │   Agent      │  │   Agent      │  │   Agent      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐                                                       │
│  │ Grafana Loki  │                                                       │
│  └──────────────┘                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

## Log Levels

### Standard Levels
| Level | Usage |
|-------|-------|
| DEBUG | Development only, verbose |
| INFO | Operational events, user actions |
| WARNING | Recoverable issues, retry attempts |
| ERROR | Errors requiring attention |
| CRITICAL | System-threatening, immediate response |

### Service-Specific Levels
- **Trading Service**: INFO minimum (critical operations)
- **Strategy Service**: INFO minimum (model operations)
- **Market Data Service**: WARNING minimum (volume optimized)
- **User Service**: INFO minimum (audit trail)

## Log Format

### Structured JSON Format
```json
{
  "timestamp": "2024-01-01T00:00:00.000Z",
  "level": "INFO",
  "service": "trading-service",
  "correlation_id": "uuid",
  "event_id": "uuid",
  "message": "Order placed successfully",
  "user_id": "uuid",
  "strategy_id": "uuid",
  "symbol": "BTCUSDT",
  "quantity": "0.01",
  "extras": {
    "exchange": "binance",
    "order_type": "market"
  }
}
```

### Field Definitions
| Field | Type | Description |
|-------|------|-------------|
| timestamp | ISO datetime | Log timestamp |
| level | string | Log level |
| service | string | Source service |
| correlation_id | UUID | Request trace |
| event_id | UUID | Event identifier |
| message | string | Log message |
| user_id | UUID | User context |
| extras | object | Additional context |

## Log Destinations

### Primary: Loki
- Centralized log aggregation
- Query-friendly format
- Retention: 30 days
- Indexes on correlation_id

### Secondary: Elasticsearch (Future)
- Full-text search
- Long-term retention
- Compliance archive

### Local: Stdout/Files
- Development debugging
- Container stdout
- Immediate access

## Sampling Strategy

### Adaptive Sampling
```python
class AdaptiveSampler:
    def should_sample(
        self,
        level: LogLevel,
        message: str,
    ) -> bool:
        """Sample based on level and rate."""
        if level >= LogLevel.ERROR:
            return True  # Always log errors
        if level >= LogLevel.WARNING:
            return random.random() < 0.1  # 10% sample
        return random.random() < 0.01  # 1% sample
```

### Volume Limits
- Max 10,000 logs/second per service
- Burst to 50,000 allowed
- Overflow drops oldest
- Alert on sustained overflow

## Log Categories

### Audit Logs
```python
AUDIT_EVENTS = [
    "strategy_created",
    "strategy_activated",
    "order_placed",
    "position_closed",
    "user_registered",
]
```

### Security Logs
```python
SECURITY_EVENTS = [
    "auth_failure",
    "auth_success",
    "rate_limit_hit",
    "invalid_input",
]
```

### Operational Logs
```python
OPERATIONAL_EVENTS = [
    "service_started",
    "service_stopped",
    "health_check",
    "config_changed",
]
```

## Compliance

### GDPR Compliance
- No personal data in logs
- User ID hashed in debug logs
- 30-day retention default
- Right to erasure supported

### PCI DSS Considerations
- No payment data in logs
- Encrypted log transmission
- Access logging
- Tamper detection

## Related Documents
- [31_OBSERVABILITY.md](31_OBSERVABILITY.md)
- [29_LOGGING.md](29_LOGGING.md)
- [15_SECURITY.md](15_SECURITY.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: DevOps Team*
*Source of Truth: docs/29_LOGGING.md*
*Depends On: 31_OBSERVABILITY.md, 29_LOGGING.md, 15_SECURITY.md*
*Related Documents: 31_OBSERVABILITY.md, 29_LOGGING.md, 15_SECURITY.md*
*Phase: Infrastructure*
