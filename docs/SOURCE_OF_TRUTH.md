---
status: Approved
owner: Architecture Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/SOURCE_OF_TRUTH.md
depends_on: []
related_documents: []
---

# QuantX AI - Source of Truth Matrix

## Purpose

This document defines exactly one authoritative document for every major topic in the QuantX AI knowledge base. When two documents conflict, this matrix determines which is correct.

**Rule: Never allow two different documents to become the source of truth for the same topic.**

## How to Use This Matrix

- If you need to update information about a topic, update the Source of Truth document.
- Other documents that reference the topic must link to the Source of Truth.
- If a document is not listed here, it is the source of truth for its own topic by default.

## Topic-to-Document Mappings

### System Foundation

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Project Overview | `01_PROJECT_OVERVIEW.md` | Mission, vision, scope, stakeholders |
| System Architecture | `02_SYSTEM_ARCHITECTURE.md` | High-level architecture, context, quality attributes |
| Technology Stack | `04_TECH_STACK.md` | All technology selections and versions |
| Project Conventions | `45_PROJECT_CONVENTIONS.md` | Architectural and coding principles |
| Coding Standard | `43_CODING_STANDARD.md` | Python code style and standards |
| Folder Structure | `44_FOLDER_STRUCTURE.md` | Repository layout |

### Architecture Decisions

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Architecture Decisions | `03_ARCHITECTURE_DECISION_RECORDS.md` | ADRs for major technical choices |
| Clean Architecture | `06_CLEAN_ARCHITECTURE.md` | Layer definitions, dependency rules |
| Service Boundaries | `07_SERVICE_BOUNDARIES.md` | Service catalog, Bounded Contexts |
| Domain Model | `05_DOMAIN_MODEL.md` | Entities, value objects, aggregates |
| Component Diagrams | `58_COMPONENT_DIAGRAMS.md` | Component architecture views |

### Data Layer

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Database Design | `08_DATABASE_DESIGN.md` | Polyglot persistence rationale |
| Database Schema | `09_DATABASE_SCHEMA.md` | Table and collection DDL |
| Entity Relationships | `10_ENTITY_RELATIONSHIP.md` | ERD and cardinality |
| Cache Strategy | `25_CACHE_STRATEGY.md` | Redis patterns, invalidation |

### AI and Machine Learning

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| AI Architecture | `17_AI_ARCHITECTURE.md` | Model types, training pipeline, inference |
| AI Pipeline | `18_AI_PIPELINE.md` | Orchestration, batch vs real-time |

### API and Contracts

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| API Specification | `11_API_SPECIFICATION.md` | REST endpoints, WebSocket, versioning |
| API Contracts | `12_API_CONTRACTS.md` | JSON schemas, event contracts, validation |

### Security

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Authentication | `13_AUTHENTICATION.md` | JWT, Telegram auth, session management |
| Authorization | `14_AUTHORIZATION.md` | RBAC, tiers, policy enforcement |
| Security Architecture | `15_SECURITY.md` | Network, encryption, compliance, incident response |

### Trading and Risk

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Risk Management | `16_RISK_MANAGEMENT.md` | Position sizing, VaR, exposure limits |
| Exchange Integration | `19_EXCHANGE_INTEGRATION.md` | Binance, Coinbase, Kraken adapters |

### Infrastructure

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Backend Architecture | `22_BACKEND_ARCHITECTURE.md` | FastAPI services, DI, caching |
| Frontend Architecture | `21_FRONTEND_ARCHITECTURE.md` | Next.js, Zustand, TanStack Table |
| Telegram Architecture | `20_TELEGRAM_ARCHITECTURE.md` | aiogram bot, FSM, handlers |
| Background Workers | `23_BACKGROUND_WORKERS.md` | Worker types, scheduling, scaling |
| Message Queue | `24_MESSAGE_QUEUE.md` | RabbitMQ cluster, routing, DLX |
| Event System | `26_EVENT_SYSTEM.md` | Domain events, event bus, outbox |
| Configuration | `27_CONFIGURATION.md` | Env vars, Vault, feature flags |
| Dependency Injection | `28_DEPENDENCY_INJECTION.md` | Container patterns, lifecycle |

### Observability

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Logging | `29_LOGGING.md` | Log format, levels, destinations |
| Monitoring | `30_MONITORING.md` | Prometheus metrics, alerting rules |
| Observability | `31_OBSERVABILITY.md` | OpenTelemetry, distributed tracing |

### Quality and Reliability

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Error Handling | `32_ERROR_HANDLING.md` | Error taxonomy, hierarchy, response format |
| Validation | `33_VALIDATION.md` | Pydantic, business rules, integrity |
| Testing | `34_TESTING.md` | pytest, coverage, quality gates |
| Performance | `35_PERFORMANCE.md` | Latency, throughput, optimization |
| Scalability | `36_SCALABILITY.md` | Horizontal scaling, sharding, capacity |

### Deployment and Operations

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Deployment | `37_DEPLOYMENT.md` | Environments, blue-green, canary |
| Docker | `38_DOCKER.md` | Multi-stage builds, scanning, registry |
| Kubernetes | `39_KUBERNETES.md` | EKS, namespaces, manifests |
| CI/CD | `40_CI_CD.md` | GitHub Actions, quality gates |
| Git Workflow | `41_GIT_WORKFLOW.md` | Branching, commits, PRs |
| Branching Strategy | `42_BRANCHING_STRATEGY.md` | GitFlow-adapted, protection rules |
| Backup and Recovery | `48_BACKUP_AND_RECOVERY.md` | Schedules, retention, PITR |
| Disaster Recovery | `49_DISASTER_RECOVERY.md` | RTO/RPO, failover, continuity |

### Process and Governance

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Sprint Planning | `52_SPRINT_PLANNING.md` | Cadence, DoD, estimation |
| Product Roadmap | `53_PRODUCT_ROADMAP.md` | Quarterly roadmap, priorities |
| Milestones | `54_MILESTONES.md` | MVP, AI, Multi-Exchange, Scale |
| Non-Functional Requirements | `55_NON_FUNCTIONAL_REQUIREMENTS.md` | NFR targets by category |
| Release Process | `50_RELEASE_PROCESS.md` | Release types, checklists |
| Versioning | `51_VERSIONING.md` | Semver, API versioning, deprecation |
| Documentation Rules | `DOCUMENTATION_RULES.md` | Writing, naming, Markdown standards |
| Documentation Templates | `DOCUMENTATION_TEMPLATE.md` | Reusable doc templates |
| Documentation Governance | `DOCUMENTATION_GOVERNANCE.md` | Lifecycle, review, ownership |
| Documentation Changelog | `DOCUMENTATION_CHANGELOG.md` | Documentation version history |

### Visualization

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Sequence Diagrams | `56_SEQUENCE_DIAGRAMS.md` | Strategy creation, order execution |
| Activity Diagrams | `57_ACTIVITY_DIAGRAMS.md` | Strategy lifecycle workflow |
| Data Flow Diagrams | `59_DATA_FLOW_DIAGRAMS.md` | Market data pipeline |
| Use Case Diagrams | `60_USE_CASE_DIAGRAMS.md` | User, bot, exchange actors |

### Operations

| Topic | Source of Truth | Description |
|-------|----------------|-------------|
| Development Guide | `46_DEVELOPMENT_GUIDE.md` | Local setup, workflow, commands |
| Operations Runbook | `47_OPERATIONS_RUNBOOK.md` | Daily checks, incident response |

## Non-Negotiable Rules

1. If a topic is not listed above, the document that first defines it is the source of truth until explicitly designated otherwise.
2. When creating a new document, add it to this matrix.
3. When deprecating a document, update this matrix to point to the replacement.
4. If two documents conflict, the one listed here wins. The other must be updated to reference the source of truth.
5. This matrix is maintained by the Architecture Team.

## Related Documents

- [DOCUMENTATION_RULES.md](DOCUMENTATION_RULES.md)
- [DOCUMENTATION_TEMPLATE.md](DOCUMENTATION_TEMPLATE.md)
- [DOCUMENTATION_GOVERNANCE.md](DOCUMENTATION_GOVERNANCE.md)
- [DOCUMENTATION_VALIDATION.md](DOCUMENTATION_VALIDATION.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Architecture Team*
*Source of Truth: docs/SOURCE_OF_TRUTH.md*
*Depends On: *
*Related Documents: *
*Phase: Foundation*
