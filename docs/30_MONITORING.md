---
status: Approved
owner: DevOps Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/30_MONITORING.md
depends_on:
  - docs/31_OBSERVABILITY.md
  - docs/29_LOGGING.md
  - docs/47_OPERATIONS_RUNBOOK.md
related_documents:
  - docs/31_OBSERVABILITY.md
  - docs/29_LOGGING.md
  - docs/47_OPERATIONS_RUNBOOK.md
---
# QuantX AI - Monitoring

## Overview

This document defines the monitoring architecture for QuantX AI, including metrics collection, alerting, dashboards, and incident detection.

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Monitoring Stack                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │   Service    │  │   Service    │  │   Service    │                 │
│   │   Metrics    │  │   Metrics    │  │   Metrics    │                 │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│          │                 │                 │                         │
│   ┌──────▼────────────────────────────────────────────────────────┐    │
│   │                    Prometheus Server                            │    │
│   │  Scrapes metrics, evaluates alerts, stores time-series data     │    │
│   └─────────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Alert-     │  │   Grafana    │  │   Service    │  │   Service    │ │
│  │   Manager    │  │   Dashboard  │  │   Health     │  │   Metrics    │ │
│   │  Exporter    │  │              │  │   Checker    │  │   UI         │ │
│   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Metrics Categories

### Business Metrics
| Metric | Type | Description |
|--------|------|-------------|
| strategies_created_total | Counter | New strategies |
| strategies_active | Gauge | Active strategies |
| positions_opened_total | Counter | Positions opened |
| positions_closed_total | Counter | Positions closed |
| orders_placed_total | Counter | Orders placed |
| revenue_mrr | Gauge | Monthly recurring revenue |
| predictions_accuracy | Gauge | Model accuracy |

### System Metrics
| Metric | Type | Description |
|--------|------|-------------|
| http_requests_total | Counter | HTTP requests |
| http_request_duration_seconds | Histogram | Request latency |
| http_request_size_bytes | Histogram | Request size |
| database_connections | Gauge | DB connections |
| redis_connections | Gauge | Redis connections |
| message_queue_depth | Gauge | Queue messages |

### Infrastructure Metrics
| Metric | Type | Description |
|--------|------|-------------|
| cpu_usage_percent | Gauge | CPU utilization |
| memory_usage_bytes | Gauge | Memory used |
| disk_usage_percent | Gauge | Disk utilization |
| network_bytes_total | Counter | Network traffic |
| container_restarts_total | Counter | Container restarts |

## Alerting Rules

### Critical Alerts
```yaml
- alert: OrderExecutionFailure
  expr: rate(quantx_orders_failed_total[5m]) > 0.05
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Order execution failing"
    description: "More than 5% of orders are failing"

- alert: ModelAccuracyLow
  expr: quantx_prediction_accuracy < 0.6
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Model accuracy below threshold"
```

### Warning Alerts
```yaml
- alert: HighLatency
  expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
  for: 5m
  labels:
    severity: warning
```

## Dashboard Design

### Service Overview Dashboard
- Request rate per service
- Error rate per service
- Latency percentiles
- Resource utilization

### Trading Dashboard
- Orders per second
- Position count
- P&L by symbol
- Risk metrics

### AI Dashboard
- Prediction accuracy
- Model latency
- Feature drift
- Confidence distribution

## Related Documents
- [31_OBSERVABILITY.md](31_OBSERVABILITY.md)
- [29_LOGGING.md](29_LOGGING.md)
- [47_OPERATIONS_RUNBOOK.md](47_OPERATIONS_RUNBOOK.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: DevOps Team*
*Source of Truth: docs/30_MONITORING.md*
*Depends On: 31_OBSERVABILITY.md, 29_LOGGING.md, 47_OPERATIONS_RUNBOOK.md*
*Related Documents: 31_OBSERVABILITY.md, 29_LOGGING.md, 47_OPERATIONS_RUNBOOK.md*
*Phase: Infrastructure*
