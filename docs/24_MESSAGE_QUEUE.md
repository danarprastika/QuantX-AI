---
status: Approved
owner: DevOps Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/24_MESSAGE_QUEUE.md
depends_on:
  - docs/23_BACKGROUND_WORKERS.md
  - docs/07_SERVICE_BOUNDARIES.md
  - docs/32_ERROR_HANDLING.md
related_documents:
  - docs/23_BACKGROUND_WORKERS.md
  - docs/07_SERVICE_BOUNDARIES.md
  - docs/32_ERROR_HANDLING.md
---
# QuantX AI - Message Queue

## Overview

This document defines the message queue architecture for QuantX AI using RabbitMQ for reliable asynchronous communication between services.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Message Queue Architecture                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │   Strategy   │  │   Trading    │  │   Market     │  │   User       │ │
│   │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
├─────────────────────────────────────────────────────────────────────────┤
│                    RabbitMQ Cluster (3 nodes)                             │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Strategy   │  │   Trading    │  │   Market     │  │   User       │ │
│  │   Workers    │  │   Workers    │  │   Workers    │  │   Workers    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## RabbitMQ Configuration

### Cluster Setup
- **Nodes**: 3 (active-active)
- **Quorum Queues**: For durability
- **Mirroring**: All queues mirrored
- **TLS**: All connections encrypted

### Connection Settings
```python
RABBITMQ_CONFIG = {
    "hosts": ["mq1.quantx.internal", "mq2.quantx.internal", "mq3.quantx.internal"],
    "port": 5672,
    "username": "quantx_service",
    "virtual_host": "/quantx",
    "heartbeat": 60,
    "blocked_timeout": 300,
}
```

## Exchange Types

### Topic Exchange (Primary)
- Pattern-based routing
- Flexible subscription
- Used for domain events

### Direct Exchange (Secondary)
- Exact routing key match
- Used for worker queues
- High performance

### Fanout Exchange (Tertiary)
- Broadcast to all subscribers
- Used for system alerts
- No routing key required

## Queue Design

### Service Queues
| Queue | Type | Purpose | TTL | Max Length |
|-------|------|---------|-----|------------|
| strategy.commands | Quorum | Strategy commands | 1h | 10,000 |
| trading.orders | Quorum | Order commands | 30m | 50,000 |
| market.data | Quorum | Market data events | 5m | 100,000 |
| user.events | Quorum | User events | 1h | 10,000 |
| notifications | Quorum | User notifications | 30m | 50,000 |
| workers.dlq | Quorum | Dead letter queue | 24h | 100,000 |

### Queue Configuration
```python
QUEUE_CONFIG = {
    "durable": True,
    "auto_delete": False,
    "exclusive": False,
    "arguments": {
        "x-message-ttl": 3600000,  # 1 hour
        "x-max-length": 100000,
        "x-queue-type": "quorum",
        "x-quorum-initial-group-size": 3,
        "x-dead-letter-exchange": "dlx",
    }
}
```

## Routing Keys

### Event Routing
```
strategy.created          → strategy.events
strategy.activated       → trading.strategy_activated
strategy.paused          → trading.strategy_paused
position.opened          → trading.position_opened
position.closed          → portfolio.position_closed
order.submitted          → trading.order_submitted
order.filled             → notification.order_filled
prediction.generated     → trading.prediction_generated
user.registered          → user.user_registered
```

### Worker Routing
```
worker.prediction.high   → strategy.prediction (high priority)
worker.prediction.low    → strategy.prediction (low priority)
worker.position.sync     → trading.position_sync
worker.order.sync        → trading.order_sync
```

## Message Serialization

### JSON Schema
```json
{
  "message_id": "uuid",
  "correlation_id": "uuid",
  "event_type": "strategy_created",
  "source_service": "strategy-service",
  "target_service": "trading-service",
  "timestamp": "2024-01-01T00:00:00Z",
  "payload": { ... },
  "schema_version": "1.0"
}
```

### Schema Evolution
- Versioned schemas stored in `/schemas/events/`
- Backward compatible changes only
- Migration on deserialization
- Schema registry (planned)

## Reliability Patterns

### Publisher Confirms
```python
async def publish_with_confirm(
    channel: aio_pika.RobustChannel,
    exchange: aio_pika.RobustExchange,
    message: WorkerMessage,
) -> bool:
    """Publish message with confirmation."""
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=message.json().encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            message_id=str(message.message_id),
        ),
        routing_key=message.routing_key,
    )
    
    # Wait for confirmation
    return await channel.wait_for_confirms()
```

### Consumer Acknowledgments
```python
async def handle_message(
    message: aio_pika.IncomingMessage,
) -> None:
    """Handle message with manual ack."""
    async with message.process(requeue=False):
        try:
            await process_event(message.body)
        except Exception as e:
            if should_retry(message.headers.get("retry_count", 0)):
                # Requeue with incremented count
                await requeue_with_delay(message, delay=5)
            else:
                await publish_to_dlq(message, error=str(e))
```

## Error Handling

### Dead Letter Exchange
```python
# DLX configuration
DLX_CONFIG = {
    "exchange": "dlx.topic",
    "queue": "workers.dlq",
    "routing_key": "#",  # Catch all
}
```

### Retry with Delay
- Delay exchange pattern
- Exponential backoff
- Max 3 retries
- Then DLQ

## Monitoring

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Queue Depth | Messages waiting | >10,000 |
| Publish Rate | Messages/sec sent | N/A |
| Consume Rate | Messages/sec processed | N/A |
| Unacked Messages | In-flight messages | >5,000 |
| Connection Count | Active connections | >50 |

### Prometheus Exporter
```python
RABBITMQ_METRICS = {
    "messages_published_total": Counter(
        "quantx_mq_published_total",
        "Messages published",
        ["exchange", "routing_key"]
    ),
    "messages_consumed_total": Counter(
        "quantx_mq_consumed_total",
        "Messages consumed",
        ["queue"]
    ),
}
```

## Related Documents
- [23_BACKGROUND_WORKERS.md](23_BACKGROUND_WORKERS.md)
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [32_ERROR_HANDLING.md](32_ERROR_HANDLING.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: DevOps Team*
*Source of Truth: docs/24_MESSAGE_QUEUE.md*
*Depends On: 23_BACKGROUND_WORKERS.md, 07_SERVICE_BOUNDARIES.md, 32_ERROR_HANDLING.md*
*Related Documents: 23_BACKGROUND_WORKERS.md, 07_SERVICE_BOUNDARIES.md, 32_ERROR_HANDLING.md*
*Phase: Infrastructure*
