---
status: Approved
owner: Architecture Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/02_SYSTEM_ARCHITECTURE.md
depends_on:
  - docs/01_PROJECT_OVERVIEW.md
  - docs/06_CLEAN_ARCHITECTURE.md
  - docs/07_SERVICE_BOUNDARIES.md
  - docs/22_BACKEND_ARCHITECTURE.md
  - docs/37_DEPLOYMENT.md
related_documents:
  - docs/01_PROJECT_OVERVIEW.md
  - docs/06_CLEAN_ARCHITECTURE.md
  - docs/07_SERVICE_BOUNDARIES.md
  - docs/22_BACKEND_ARCHITECTURE.md
  - docs/37_DEPLOYMENT.md
---
# QuantX AI - System Architecture

## Architectural Overview

QuantX AI follows a **modular layered architecture** with clean separation of concerns. The system is designed for high availability, low-latency trading operations, and horizontal scalability.

### Architecture Style
- **Primary**: Clean Architecture (Onion/Hexagonal)
- **Secondary**: Microservices pattern for independent scaling
- **Integration**: Event-driven architecture for async processing

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL INTERFACES                               │
├─────────────────────────────────────────────────────────────────────────────┤
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │   Telegram   │    │   REST API   │    │   WebSocket  │                 │
│   │     Bot      │    │   Clients    │    │   Stream     │                 │
│   └──────────────┘    └──────────────┘    └──────────────┘                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                           PRESENTATION LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │              API Gateway / Load Balancer (Traefik/Nginx)             │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────────┤
│                           APPLICATION LAYER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Strategy    │  │   Trading    │  │   Market     │  │   User &     │   │
│  │  Service     │  │   Service    │  │  Data        │  │  Auth        │   │
│  │              │  │              │  │   Service    │  │   Service    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
├─────────────────────────────────────────────────────────────────────────────┤
│                           DOMAIN LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          Shared Core Domain                          │   │
│  │  Strategies, Positions, Orders, Predictions, Portfolios             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────────┤
│                           INFRASTRUCTURE LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Exchange    │  │   Telegram   │  │    Cache     │  │  Message     │   │
│  │  Adapters    │  │   Adapters   │  │  (Redis)     │  │   Queue      │   │
│  │              │  │              │  │              │  │  (RabbitMQ)  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
├─────────────────────────────────────────────────────────────────────────────┤
│                           DATA LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Primary    │  │   Timescale  │  │   MongoDB    │  │    S3      │   │
│  │   PostgreSQL │  │   (Market    │  │   (Events &  │  │  (Archives) │   │
│  │   (Core DB)  │  │    Data)     │  │   Sessions)  │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## System Context

### External Systems
| System | Integration Type | Purpose | SLA |
|--------|-----------------|---------|-----|
| Binance API | REST/WebSocket | Trading, market data | 99.9% |
| Coinbase Pro API | REST/WebSocket | Trading, market data | 99.9% |
| Kraken API | REST/WebSocket | Trading, market data | 99.9% |
| Telegram API | HTTPS | User interaction | 99.5% |
| Stripe API | HTTPS | Billing | 99.9% |
| AWS S3 | S3 API | Data archival | 99.99% |

### Data Flow Overview
1. Market data ingested from exchanges via WebSocket streams
2. Data normalized and stored in TimescaleDB
3. AI models consume market data for predictions
4. Trading service evaluates signals and executes orders
5. Results pushed to users via Telegram or WebSocket
6. All events persisted to MongoDB for audit trail

## Quality Attributes

### Scalability
- **Horizontal**: Services scale independently via container orchestration
- **Vertical**: Database sharding by exchange/symbol
- **Load Handling**: 10,000 concurrent users, 1M predictions/day

### Performance
- **Latency Target**: <50ms order execution
- **Throughput**: 10,000 messages/second
- **Cold Start**: <5 seconds for service initialization

### Availability
- **Target**: 99.9% uptime for trading operations
- **Redundancy**: Multi-zone deployment
- **Failover**: Automatic within 30 seconds

### Security
- **Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Auth**: JWT tokens with refresh rotation
- **Auditing**: Full audit trail of all operations

## Deployment Architecture

### Production Environment
- **Cloud Provider**: AWS (primary), Azure (backup)
- **Region**: us-east-1 (primary), us-west-2 (backup)
- **Network**: VPC with private subnets for services
- **Load Balancer**: Application Load Balancer
- **CDN**: CloudFront for static assets

### Staging Environment
- **Isolation**: Separate VPC with identical architecture
- **Data**: Anonymized production data subset
- **Purpose**: Pre-production validation

## Technology Distribution

| Layer | Technology | Rationale |
|-------|------------|-----------|
| API Gateway | Traefik | Dynamic routing, middleware support |
| Services | Python/FastAPI | Async support, ML ecosystem |
| Message Queue | RabbitMQ | AMQP protocol, reliability |
| Cache | Redis | Pub/Sub, low-latency caching |
| Primary DB | PostgreSQL | ACID, JSONB support |
| Time Series | TimescaleDB | Compression, time-based queries |
| Document DB | MongoDB | Event store flexibility |
| Containerization | Docker | Portability, consistency |
| Orchestration | Kubernetes | Auto-scaling, self-healing |
| Monitoring | Prometheus + Grafana | Metrics collection and visualization |

## Service Boundaries Summary

See [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md) for detailed service definitions.

## Related Documents
- [01_PROJECT_OVERVIEW.md](01_PROJECT_OVERVIEW.md)
- [06_CLEAN_ARCHITECTURE.md](06_CLEAN_ARCHITECTURE.md)
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [22_BACKEND_ARCHITECTURE.md](22_BACKEND_ARCHITECTURE.md)
- [37_DEPLOYMENT.md](37_DEPLOYMENT.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Architecture Team*
*Source of Truth: docs/02_SYSTEM_ARCHITECTURE.md*
*Depends On: 01_PROJECT_OVERVIEW.md, 06_CLEAN_ARCHITECTURE.md, 07_SERVICE_BOUNDARIES.md, 22_BACKEND_ARCHITECTURE.md, 37_DEPLOYMENT.md*
*Related Documents: 01_PROJECT_OVERVIEW.md, 06_CLEAN_ARCHITECTURE.md, 07_SERVICE_BOUNDARIES.md, 22_BACKEND_ARCHITECTURE.md, 37_DEPLOYMENT.md*
*Phase: Foundation*
