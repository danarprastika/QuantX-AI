# QuantX AI - Observability

## Overview

This document defines the observability architecture for QuantX AI, including distributed tracing, metrics, logging correlation, and diagnostic capabilities.

## Observability Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Observability Stack                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │   Service    │  │   Service    │  │   Service    │                 │
│   │   Traces     │  │   Traces     │  │   Traces     │                 │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│          │                 │                 │                         │
│   ┌──────▼────────────────────────────────────────────────────────┐    │
│   │                    OpenTelemetry Collector                     │    │
│   │  Receives traces, metrics, logs, exports to backends         │    │
│   └─────────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Jaeger     │  │   Prometheus │  │   Loki       │  │   Grafana    │ │
│  │   (Traces)   │  │   (Metrics)  │  │   (Logs)     │  │   (Unified)  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Distributed Tracing

### Trace Context Propagation
```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind

tracer = trace.get_tracer("quantx-trading")

@tracer.start_as_current_span("place_order", kind=SpanKind.CLIENT)
async def place_order(order: Order) -> ExchangeOrder:
    span = trace.get_current_span()
    span.set_attribute("order.symbol", order.symbol.value)
    span.set_attribute("order.quantity", float(order.quantity))
    span.set_attribute("order.type", order.type.value)
    
    try:
        result = await exchange_client.submit(order)
        span.set_attribute("order.exchange_id", result.id)
        return result
    except Exception as e:
        span.record_exception(e)
        span.set_status(Status(StatusCode.ERROR, str(e)))
        raise
```

### Span Attributes
| Attribute | Type | Description |
|-----------|------|-------------|
| service.name | string | Service identifier |
| service.version | string | Version number |
| user.id | string | User UUID |
| correlation_id | string | Request correlation |
| strategy.id | string | Strategy UUID |
| position.id | string | Position UUID |

### Trace Sampling
- 100% for errors
- 10% for slow requests (>1s)
- 1% for normal traffic
- Configurable by service

## Correlation

### Correlation ID Flow
```
Request → Correlation ID (UUID) → All logs/metrics/traces
```

### Span Linking
```python
# Link related spans
span.link_to_parent(SpanContext(correlation_id))
span.add_event("prediction_generated", attributes={"model_id": model_id})
```

## Service Mesh Integration
- Istio sidecar for each service
- Automatic trace propagation
- mTLS enforcement
- Traffic metrics

## Related Documents
- [30_MONITORING.md](30_MONITORING.md)
- [29_LOGGING.md](29_LOGGING.md)
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Infrastructure*