---
status: Approved
owner: DevOps Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/23_BACKGROUND_WORKERS.md
depends_on:
  - docs/24_MESSAGE_QUEUE.md
  - docs/32_ERROR_HANDLING.md
  - docs/30_MONITORING.md
related_documents:
  - docs/24_MESSAGE_QUEUE.md
  - docs/32_ERROR_HANDLING.md
  - docs/30_MONITORING.md
---
# QuantX AI - Background Workers

## Overview

This document defines the background worker architecture for QuantX AI, including worker types, scheduling, deployment, monitoring, and failure handling.

## Worker Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Worker Architecture                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │   Scheduler  │  │   Worker     │  │   Worker     │  │   Worker     │ │
│   │   (Cron/AQ)  │  │   Pool       │  │   Pool       │  │   Pool       │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼─────────────────────────────────────────────────────────────┐    │
│   │                    Message Queue (RabbitMQ)                          │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │    │
│   │  │ Strategy │  │ Trading  │  │ Market   │  │ User     │         │    │
│   │  │ Queue    │  │ Queue    │  │ Queue    │  │ Queue    │         │    │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Strategy   │  │   Trading    │  │   Market     │  │   User       │ │
│  │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Worker Types

### Core Workers

#### PredictionWorker
- **Purpose**: Generate AI predictions for active strategies
- **Schedule**: Continuous (triggered by market data)
- **Concurrency**: Per-symbol parallelism
- **Priority**: High

#### PositionSyncWorker
- **Purpose**: Sync position status from exchanges
- **Schedule**: Every 30 seconds
- **Concurrency**: Per-exchange parallelism
- **Priority**: High

#### OrderSyncWorker
- **Purpose**: Sync order status from exchanges
- **Schedule**: Every 5 seconds
- **Concurrency**: Per-exchange parallelism
- **Priority**: Critical

#### RiskMonitorWorker
- **Purpose**: Monitor risk metrics and trigger alerts
- **Schedule**: Every 10 seconds
- **Concurrency**: Per-user parallelism
- **Priority**: Critical

### Maintenance Workers

#### CleanupWorker
- **Purpose**: Clean up expired sessions, old data
- **Schedule**: Daily at 03:00 UTC
- **Concurrency**: Single instance
- **Priority**: Low

#### BackupWorker
- **Purpose**: Create database backups
- **Schedule**: Daily at 02:00 UTC
- **Concurrency**: Single instance
- **Priority**: High

#### ReportWorker
- **Purpose**: Generate user reports
- **Schedule**: On-demand + weekly summary
- **Concurrency**: Per-user parallelism
- **Priority**: Low

### Support Workers

#### HealthCheckWorker
- **Purpose**: Check exchange connectivity
- **Schedule**: Every 60 seconds
- **Concurrency**: Per-exchange
- **Priority**: Medium

#### CacheWarmWorker
- **Purpose**: Warm cache with frequently accessed data
- **Schedule**: On service startup + hourly
- **Concurrency**: Configurable
- **Priority**: Low

## Worker Deployment

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prediction-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prediction-worker
  template:
    metadata:
      labels:
        app: prediction-worker
    spec:
      containers:
      - name: worker
        image: quantx/worker:prediction-latest
        envFrom:
        - configMapRef:
            name: quantx-config
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### Worker Scaling
| Worker | Min Replicas | Max Replicas | Scaling Trigger |
|--------|--------------|--------------|-----------------|
| Prediction | 2 | 10 | Active strategies |
| PositionSync | 2 | 5 | Exchange load |
| OrderSync | 3 | 10 | Pending orders |
| RiskMonitor | 2 | 8 | Active positions |

## Worker Configuration

### Configuration Schema
```python
class WorkerConfig(BaseSettings):
    worker_type: WorkerType
    concurrency: int = 10
    batch_size: int = 100
    poll_interval: float = 1.0
    max_retries: int = 3
    retry_delay: float = 5.0
    dead_letter_queue: str = "worker-dlq"
    
    class Config:
        env_prefix = "QUANTX_WORKER_"
```

### Environment Variables
```
QUANTX_WORKER_TYPE=prediction
QUANTX_WORKER_CONCURRENCY=10
QUANTX_WORKER_BATCH_SIZE=100
QUANTX_WORKER_POLL_INTERVAL=1.0
QUANTX_WORKER_MAX_RETRIES=3
```

## Message Queue Integration

### Queue Naming Convention
```
{service}.{worker-type}
strategy.prediction
trading.position-sync
trading.order-sync
market.data-collector
```

### Message Format
```json
{
  "message_id": "uuid",
  "correlation_id": "uuid",
  "worker_type": "prediction",
  "payload": {
    "strategy_id": "uuid",
    "symbol": "BTCUSDT"
  },
  "priority": 5,
  "scheduled_for": "2024-01-01T00:00:00Z"
}
```

### Priority Levels
| Priority | Purpose |
|----------|---------|
| 1-3 | Critical (order sync) |
| 4-6 | High (predictions, risk) |
| 7-9 | Medium (position sync) |
| 10 | Low (cleanup, reports) |

## Error Handling

### Retry Strategy
```python
async def process_with_retry(
    worker: BaseWorker,
    message: WorkerMessage,
    max_retries: int = 3,
) -> None:
    for attempt in range(max_retries):
        try:
            await worker.process(message)
            return
        except TransientError as e:
            delay = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
        except PermanentError as e:
            await send_to_dlq(message, str(e))
            return
    
    await send_to_dlq(message, "Max retries exceeded")
```

### Dead Letter Queue
- Messages after max retries
- Permanent errors
- Invalid message format
- Poison message detection

### Poison Message Detection
```python
class PoisonMessageDetector:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
    
    async def is_poison(self, message: WorkerMessage) -> bool:
        key = f"poison:{message.worker_type}:{hash(message.payload)}"
        count = await self.redis.incr(key)
        await self.redis.expire(key, 3600)
        
        if count > 100:  # Same message failed 100 times
            return True
        return False
```

## Monitoring

### Worker Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Queue Depth | Pending messages | >1000 |
| Processing Time | Avg per message | >1s |
| Error Rate | Failed messages | >1% |
| Memory Usage | Worker memory | >80% |
| CPU Usage | Worker CPU | >80% |

### Prometheus Metrics
```python
WORKER_MESSAGES_PROCESSED = Counter(
    "quantx_worker_messages_processed_total",
    "Messages processed by worker",
    ["worker_type", "status"]  # status: success, error, retried
)

WORKER_PROCESSING_TIME = Histogram(
    "quantx_worker_processing_seconds",
    "Processing time distribution",
    ["worker_type"]
)
```

## Worker Lifecycle

### Startup Sequence
1. Load configuration
2. Connect to message queue
3. Connect to databases
4. Connect to cache
5. Start consuming messages

### Shutdown Sequence
1. Stop consuming new messages
2. Wait for in-flight messages (30s)
3. Ack pending messages
4. Close connections
5. Exit cleanly

### Health Checks
```python
@app.get("/health")
async def health() -> dict:
    return {
        "status": "healthy",
        "queue_connected": mq.health_check(),
        "db_connected": db.health_check(),
        "cache_connected": cache.health_check(),
        "workers_active": len(active_workers),
    }
```

## Related Documents
- [24_MESSAGE_QUEUE.md](24_MESSAGE_QUEUE.md)
- [32_ERROR_HANDLING.md](32_ERROR_HANDLING.md)
- [30_MONITORING.md](30_MONITORING.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: DevOps Team*
*Source of Truth: docs/23_BACKGROUND_WORKERS.md*
*Depends On: 24_MESSAGE_QUEUE.md, 32_ERROR_HANDLING.md, 30_MONITORING.md*
*Related Documents: 24_MESSAGE_QUEUE.md, 32_ERROR_HANDLING.md, 30_MONITORING.md*
*Phase: Infrastructure*
