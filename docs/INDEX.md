---
status: Approved
owner: Architecture Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/INDEX.md
depends_on: ["docs/01_PROJECT_OVERVIEW.md", "docs/SOURCE_OF_TRUTH.md"]
related_documents:
  - docs/SOURCE_OF_TRUTH.md
  - docs/DOCUMENTATION_RULES.md
  - docs/DOCUMENTATION_TEMPLATE.md
---
# QuantX AI - Documentation Index

## Overview

This document provides a master index of all QuantX AI documentation, organized by category and reading order.

---

## 1. Document Categories

### System Foundation (Read First)

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 01 | [Project Overview](01_PROJECT_OVERVIEW.md) | Mission, vision, scope, stakeholders | 1 |
| 02 | [System Architecture](02_SYSTEM_ARCHITECTURE.md) | High-level architecture, quality attributes | 2 |
| 04 | [Technology Stack](04_TECH_STACK.md) | Technology selections and versions | 3 |
| 45 | [Project Conventions](45_PROJECT_CONVENTIONS.md) | Architectural and coding principles | 4 |
| 43 | [Coding Standard](43_CODING_STANDARD.md) | Python code style and standards | 5 |
| 44 | [Folder Structure](44_FOLDER_STRUCTURE.md) | Repository layout | 6 |
| 55 | [Non-Functional Requirements](55_NON_FUNCTIONAL_REQUIREMENTS.md) | Performance, scalability targets | 7 |

### Architecture Decisions (Read Second)

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 03 | [Architecture Decision Records](03_ARCHITECTURE_DECISION_RECORDS.md) | ADRs for major technical choices | 1 |
| 06 | [Clean Architecture](06_CLEAN_ARCHITECTURE.md) | Layer definitions, dependency rules | 2 |
| 07 | [Service Boundaries](07_SERVICE_BOUNDARIES.md) | Service catalog, Bounded Contexts | 3 |
| 05 | [Domain Model](05_DOMAIN_MODEL.md) | Entities, value objects, aggregates | 4 |
| 58 | [Component Diagrams](58_COMPONENT_DIAGRAMS.md) | Component architecture views | 5 |

### Data Layer

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 08 | [Database Design](08_DATABASE_DESIGN.md) | Polyglot persistence rationale | 1 |
| 09 | [Database Schema](09_DATABASE_SCHEMA.md) | Table and collection DDL | 2 |
| 10 | [Entity Relationship](10_ENTITY_RELATIONSHIP.md) | ERD and cardinality | 3 |
| 25 | [Cache Strategy](25_CACHE_STRATEGY.md) | Redis patterns, invalidation | 4 |

### AI and Machine Learning

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 17 | [AI Architecture](17_AI_ARCHITECTURE.md) | Model types, training pipeline, inference | 1 |
| 18 | [AI Pipeline](18_AI_PIPELINE.md) | Orchestration, batch vs real-time | 2 |

### API and Contracts

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 11 | [API Specification](11_API_SPECIFICATION.md) | REST endpoints, WebSocket, versioning | 1 |
| 12 | [API Contracts](12_API_CONTRACTS.md) | JSON schemas, event contracts, validation | 2 |

### Security

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 13 | [Authentication](13_AUTHENTICATION.md) | JWT, Telegram auth, session management | 1 |
| 14 | [Authorization](14_AUTHORIZATION.md) | RBAC, tiers, policy enforcement | 2 |
| 15 | [Security](15_SECURITY.md) | Network, encryption, compliance | 3 |

### Trading and Risk

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 16 | [Risk Management](16_RISK_MANAGEMENT.md) | Position sizing, VaR, exposure limits | 1 |
| 19 | [Exchange Integration](19_EXCHANGE_INTEGRATION.md) | Binance, Coinbase, Kraken adapters | 2 |

### Infrastructure

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 22 | [Backend Architecture](22_BACKEND_ARCHITECTURE.md) | FastAPI services, DI, caching | 1 |
| 21 | [Frontend Architecture](21_FRONTEND_ARCHITECTURE.md) | Next.js, Zustand, TanStack Table | 2 |
| 20 | [Telegram Architecture](20_TELEGRAM_ARCHITECTURE.md) | aiogram bot, FSM, handlers | 3 |
| 23 | [Background Workers](23_BACKGROUND_WORKERS.md) | Worker types, scheduling, scaling | 4 |
| 24 | [Message Queue](24_MESSAGE_QUEUE.md) | RabbitMQ cluster, routing, DLX | 5 |
| 26 | [Event System](26_EVENT_SYSTEM.md) | Domain events, event bus, outbox | 6 |
| 27 | [Configuration](27_CONFIGURATION.md) | Env vars, Vault, feature flags | 7 |
| 28 | [Dependency Injection](28_DEPENDENCY_INJECTION.md) | Container patterns, lifecycle | 8 |

### Observability

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 29 | [Logging](29_LOGGING.md) | Log format, levels, destinations | 1 |
| 30 | [Monitoring](30_MONITORING.md) | Prometheus metrics, alerting rules | 2 |
| 31 | [Observability](31_OBSERVABILITY.md) | OpenTelemetry, distributed tracing | 3 |

### Quality and Reliability

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 32 | [Error Handling](32_ERROR_HANDLING.md) | Error taxonomy, response format | 1 |
| 33 | [Validation](33_VALIDATION.md) | Pydantic, business rules, integrity | 2 |
| 34 | [Testing](34_TESTING.md) | pytest, coverage, quality gates | 3 |
| 35 | [Performance](35_PERFORMANCE.md) | Latency, throughput, optimization | 4 |
| 36 | [Scalability](36_SCALABILITY.md) | Horizontal scaling, sharding | 5 |

### Deployment and Operations

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 37 | [Deployment](37_DEPLOYMENT.md) | Environments, blue-green, canary | 1 |
| 38 | [Docker](38_DOCKER.md) | Multi-stage builds, scanning | 2 |
| 39 | [Kubernetes](39_KUBERNETES.md) | EKS, namespaces, manifests | 3 |
| 40 | [CI/CD](40_CI_CD.md) | GitHub Actions, quality gates | 4 |
| 41 | [Git Workflow](41_GIT_WORKFLOW.md) | Branching, commits, PRs | 5 |
| 42 | [Branching Strategy](42_BRANCHING_STRATEGY.md) | GitFlow-adapted, protection rules | 6 |
| 48 | [Backup and Recovery](48_BACKUP_AND_RECOVERY.md) | Schedules, retention, PITR | 7 |
| 49 | [Disaster Recovery](49_DISASTER_RECOVERY.md) | RTO/RPO, failover, continuity | 8 |

### Process and Governance

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 52 | [Sprint Planning](52_SPRINT_PLANNING.md) | Cadence, DoD, estimation | 1 |
| 53 | [Product Roadmap](53_PRODUCT_ROADMAP.md) | Quarterly roadmap, priorities | 2 |
| 54 | [Milestones](54_MILESTONES.md) | MVP, AI, Multi-Exchange, Scale | 3 |
| 50 | [Release Process](50_RELEASE_PROCESS.md) | Release types, checklists | 4 |
| 51 | [Versioning](51_VERSIONING.md) | Semver, API versioning | 5 |
| DOCUMENTATION_GOVERNANCE.md | Documentation Governance | Lifecycle, review, ownership | 6 |
| DOCUMENTATION_RULES.md | Documentation Rules | Writing, naming, Markdown standards | 7 |
| DOCUMENTATION_TEMPLATE.md | Documentation Templates | Reusable doc templates | 8 |

### Visualization

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 56 | [Sequence Diagrams](56_SEQUENCE_DIAGRAMS.md) | Strategy creation, order execution | 1 |
| 57 | [Activity Diagrams](57_ACTIVITY_DIAGRAMS.md) | Strategy lifecycle workflow | 2 |
| 59 | [Data Flow Diagrams](59_DATA_FLOW_DIAGRAMS.md) | Market data pipeline | 3 |
| 60 | [Use Case Diagrams](60_USE_CASE_DIAGRAMS.md) | User, bot, exchange actors | 4 |

### Operations

| # | Document | Purpose | Reading Order |
|---|----------|---------|---------------|
| 46 | [Development Guide](46_DEVELOPMENT_GUIDE.md) | Local setup, workflow, commands | 1 |
| 47 | [Operations Runbook](47_OPERATIONS_RUNBOOK.md) | Daily checks, incident response | 2 |

---

## 2. Source of Truth Matrix

| Topic | Source of Truth Document |
|-------|--------------------------|
| Project Overview | [01_PROJECT_OVERVIEW.md](01_PROJECT_OVERVIEW.md) |
| System Architecture | [02_SYSTEM_ARCHITECTURE.md](02_SYSTEM_ARCHITECTURE.md) |
| Technology Stack | [04_TECH_STACK.md](04_TECH_STACK.md) |
| Project Conventions | [45_PROJECT_CONVENTIONS.md](45_PROJECT_CONVENTIONS.md) |
| Coding Standard | [43_CODING_STANDARD.md](43_CODING_STANDARD.md) |
| Architecture Decisions | [03_ARCHITECTURE_DECISION_RECORDS.md](03_ARCHITECTURE_DECISION_RECORDS.md) |
| Clean Architecture | [06_CLEAN_ARCHITECTURE.md](06_CLEAN_ARCHITECTURE.md) |
| Service Boundaries | [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md) |
| Domain Model | [05_DOMAIN_MODEL.md](05_DOMAIN_MODEL.md) |
| Component Diagrams | [58_COMPONENT_DIAGRAMS.md](58_COMPONENT_DIAGRAMS.md) |
| Database Design | [08_DATABASE_DESIGN.md](08_DATABASE_DESIGN.md) |
| Database Schema | [09_DATABASE_SCHEMA.md](09_DATABASE_SCHEMA.md) |
| Entity Relationships | [10_ENTITY_RELATIONSHIP.md](10_ENTITY_RELATIONSHIP.md) |
| Cache Strategy | [25_CACHE_STRATEGY.md](25_CACHE_STRATEGY.md) |
| AI Architecture | [17_AI_ARCHITECTURE.md](17_AI_ARCHITECTURE.md) |
| AI Pipeline | [18_AI_PIPELINE.md](18_AI_PIPELINE.md) |
| API Specification | [11_API_SPECIFICATION.md](11_API_SPECIFICATION.md) |
| API Contracts | [12_API_CONTRACTS.md](12_API_CONTRACTS.md) |
| Authentication | [13_AUTHENTICATION.md](13_AUTHENTICATION.md) |
| Authorization | [14_AUTHORIZATION.md](14_AUTHORIZATION.md) |
| Security Architecture | [15_SECURITY.md](15_SECURITY.md) |
| Risk Management | [16_RISK_MANAGEMENT.md](16_RISK_MANAGEMENT.md) |
| Exchange Integration | [19_EXCHANGE_INTEGRATION.md](19_EXCHANGE_INTEGRATION.md) |
| Backend Architecture | [22_BACKEND_ARCHITECTURE.md](22_BACKEND_ARCHITECTURE.md) |
| Frontend Architecture | [21_FRONTEND_ARCHITECTURE.md](21_FRONTEND_ARCHITECTURE.md) |
| Telegram Architecture | [20_TELEGRAM_ARCHITECTURE.md](20_TELEGRAM_ARCHITECTURE.md) |
| Background Workers | [23_BACKGROUND_WORKERS.md](23_BACKGROUND_WORKERS.md) |
| Message Queue | [24_MESSAGE_QUEUE.md](24_MESSAGE_QUEUE.md) |
| Event System | [26_EVENT_SYSTEM.md](26_EVENT_SYSTEM.md) |
| Configuration | [27_CONFIGURATION.md](27_CONFIGURATION.md) |
| Dependency Injection | [28_DEPENDENCY_INJECTION.md](28_DEPENDENCY_INJECTION.md) |
| Logging | [29_LOGGING.md](29_LOGGING.md) |
| Monitoring | [30_MONITORING.md](30_MONITORING.md) |
| Observability | [31_OBSERVABILITY.md](31_OBSERVABILITY.md) |
| Error Handling | [32_ERROR_HANDLING.md](32_ERROR_HANDLING.md) |
| Validation | [33_VALIDATION.md](33_VALIDATION.md) |
| Testing | [34_TESTING.md](34_TESTING.md) |
| Performance | [35_PERFORMANCE.md](35_PERFORMANCE.md) |
| Scalability | [36_SCALABILITY.md](36_SCALABILITY.md) |
| Deployment | [37_DEPLOYMENT.md](37_DEPLOYMENT.md) |
| Docker | [38_DOCKER.md](38_DOCKER.md) |
| Kubernetes | [39_KUBERNETES.md](39_KUBERNETES.md) |
| CI/CD | [40_CI_CD.md](40_CI_CD.md) |
| Git Workflow | [41_GIT_WORKFLOW.md](41_GIT_WORKFLOW.md) |
| Branching Strategy | [42_BRANCHING_STRATEGY.md](42_BRANCHING_STRATEGY.md) |
| Backup and Recovery | [48_BACKUP_AND_RECOVERY.md](48_BACKUP_AND_RECOVERY.md) |
| Disaster Recovery | [49_DISASTER_RECOVERY.md](49_DISASTER_RECOVERY.md) |
| Sprint Planning | [52_SPRINT_PLANNING.md](52_SPRINT_PLANNING.md) |
| Product Roadmap | [53_PRODUCT_ROADMAP.md](53_PRODUCT_ROADMAP.md) |
| Milestones | [54_MILESTONES.md](54_MILESTONES.md) |
| Non-Functional Requirements | [55_NON_FUNCTIONAL_REQUIREMENTS.md](55_NON_FUNCTIONAL_REQUIREMENTS.md) |
| Release Process | [50_RELEASE_PROCESS.md](50_RELEASE_PROCESS.md) |
| Versioning | [51_VERSIONING.md](51_VERSIONING.md) |
| Documentation Rules | [DOCUMENTATION_RULES.md](DOCUMENTATION_RULES.md) |
| Documentation Templates | [DOCUMENTATION_TEMPLATE.md](DOCUMENTATION_TEMPLATE.md) |
| Documentation Governance | [DOCUMENTATION_GOVERNANCE.md](DOCUMENTATION_GOVERNANCE.md) |
| Documentation Changelog | [DOCUMENTATION_CHANGELOG.md](DOCUMENTATION_CHANGELOG.md) |
| Sequence Diagrams | [56_SEQUENCE_DIAGRAMS.md](56_SEQUENCE_DIAGRAMS.md) |
| Activity Diagrams | [57_ACTIVITY_DIAGRAMS.md](57_ACTIVITY_DIAGRAMS.md) |
| Data Flow Diagrams | [59_DATA_FLOW_DIAGRAMS.md](59_DATA_FLOW_DIAGRAMS.md) |
| Use Case Diagrams | [60_USE_CASE_DIAGRAMS.md](60_USE_CASE_DIAGRAMS.md) |
| Development Guide | [46_DEVELOPMENT_GUIDE.md](46_DEVELOPMENT_GUIDE.md) |
| Operations Runbook | [47_OPERATIONS_RUNBOOK.md](47_OPERATIONS_RUNBOOK.md) |

---

## 3. Dependency Graph (Reading Order)

```
01_PROJECT_OVERVIEW.md (Root - no dependencies)
    │
    ├── 02_SYSTEM_ARCHITECTURE.md
    │       │
    │       ├── 07_SERVICE_BOUNDARIES.md
    │       ├── 22_BACKEND_ARCHITECTURE.md
    │       └── 37_DEPLOYMENT.md
    │
    ├── 04_TECH_STACK.md (Root - no dependencies)
    │
    ├── 55_NON_FUNCTIONAL_REQUIREMENTS.md
    │
    └── 53_PRODUCT_ROADMAP.md

03_ARCHITECTURE_DECISION_RECORDS.md (Root - no dependencies)
    │
    └── 06_CLEAN_ARCHITECTURE.md
            │
            ├── 05_DOMAIN_MODEL.md
            ├── 07_SERVICE_BOUNDARIES.md
            └── 28_DEPENDENCY_INJECTION.md

05_DOMAIN_MODEL.md
    │
    ├── 08_DATABASE_DESIGN.md
    │       │
    │       ├── 09_DATABASE_SCHEMA.md
    │       └── 48_BACKUP_AND_RECOVERY.md
    │
    └── 09_DATABASE_SCHEMA.md (Self-contained after DB design)

11_API_SPECIFICATION.md
    │
    └── 12_API_CONTRACTS.md

13_AUTHENTICATION.md
    │
    └── 14_AUTHORIZATION.md
            │
            └── 15_SECURITY.md

27_CONFIGURATION.md
    │
    └── 28_DEPENDENCY_INJECTION.md
            │
            ├── 22_BACKEND_ARCHITECTURE.md
            └── 06_CLEAN_ARCHITECTURE.md
```

---

## 4. Navigation

### Quick Access

- [Source of Truth Matrix](SOURCE_OF_TRUTH.md) - Authoritative topics
- [Documentation Rules](DOCUMENTATION_RULES.md) - Writing standards
- [Documentation Templates](DOCUMENTATION_TEMPLATE.md) - Document templates
- [Documentation Governance](DOCUMENTATION_GOVERNANCE.md) - Review process
- [Documentation Changelog](DOCUMENTATION_CHANGELOG.md) - Version history

### Validation

- [Documentation Validation](DOCUMENTATION_VALIDATION.md) - QA rules
- Run `python scripts/validate_docs.py` to validate all documentation

---

## 5. Document Count by Category

| Category | Documents |
|----------|-----------|
| System Foundation | 6 |
| Architecture Decisions | 5 |
| Data Layer | 4 |
| AI and Machine Learning | 2 |
| API and Contracts | 2 |
| Security | 3 |
| Trading and Risk | 2 |
| Infrastructure | 8 |
| Observability | 3 |
| Quality and Reliability | 5 |
| Deployment and Operations | 8 |
| Process and Governance | 7 |
| Visualization | 4 |
| Operations | 2 |
| **Total** | **56** |

---

## Related Documents

- [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md)
- [DOCUMENTATION_RULES.md](DOCUMENTATION_RULES.md)