---
status: Approved
owner: Architecture Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/DOCUMENTATION_TEMPLATE.md
depends_on: ["docs/DOCUMENTATION_RULES.md"]
related_documents: []
---

# QuantX AI - Documentation Templates

## Template Usage

Copy the appropriate template below when creating a new document. Remove sections that do not apply. Do not add sections not defined in the templates.

All templates share a common metadata header. Replace placeholder values with actual content.

```yaml
---
status: Draft | In Review | Approved | Deprecated | Archived
owner: <Team or Individual>
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/XX_FILENAME.md
depends_on: []
related_documents: []
---
```

---

# {Document Title}

## 1. Purpose

<!-- Why this document exists. What problem does it solve? -->

## 2. Scope

<!-- What is covered by this document? What is explicitly out of scope? -->

## 3. Responsibilities

<!-- Who owns this document? Who is responsible for accuracy and maintenance? -->

## 4. Dependencies

<!-- What other documents, systems, or external factors does this document depend on? -->

## 5. References

<!-- External references, standards, RFCs, URLs -->

## 6. Related Documents

<!-- Links to related QuantX AI documentation -->

- [Related Document](XX_FILENAME.md)

## 7. Status

<!-- Current approval status: Draft, In Review, Approved, Deprecated, Archived -->

## 8. Owner

<!-- Team or individual responsible for this document -->

## 9. Last Updated

<!-- Date of last update (YYYY-MM-DD) -->

---

## Dedicated Templates

---

# Template: Architecture Document

```yaml
---
status: Draft
owner: Architecture Team
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/XX_FILENAME.md
depends_on: []
related_documents: []
---
```

# {System Name} - {Component} Architecture

## 1. Purpose

<!-- Describe the purpose of this architecture document. -->

## 2. Scope

<!-- What architectures and components are covered? -->

## 3. Architectural Context

<!-- How does this component fit into the overall system? -->

## 4. Architectural Style

<!--单体, microservices, event-driven, layered, etc. -->

## 5. Components and Responsibilities

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| | | |

## 6. Interfaces and Contracts

<!-- APIs, protocols, message formats -->

## 7. Data Flow

<!-- How data moves through the architecture -->

## 8. Dependencies

<!-- Internal and external dependencies -->

## 9. Quality Attributes

<!-- Scalability, availability, security, performance targets -->

## 10. Deployment Architecture

<!-- Environments, regions, topology -->

## 11. References

## 12. Related Documents

## 13. Status

## 14. Owner

## 15. Last Updated

---

# Template: API Document

```yaml
---
status: Draft
owner: Backend Team
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/11_API_SPECIFICATION.md
depends_on: ["docs/07_SERVICE_BOUNDARIES.md"]
related_documents: ["docs/12_API_CONTRACTS.md"]
---
```

# {Service Name} - API Specification

## 1. Purpose

<!-- What does this API enable? -->

## 2. Scope

<!-- Version, coverage, environments -->

## 3. Base URL and Versioning

```
{base_url}
```

## 4. Authentication

<!-- JWT, API key, OAuth... -->

## 5. Rate Limiting

<!-- Limits per endpoint or tier -->

## 6. Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "correlation_id": "uuid",
    "timestamp": "ISO8601"
  }
}
```

## 7. Endpoints

### {Method} {Path}

<!-- Description, request body, response body, status codes -->

## 8. Data Models

<!-- Pydantic models or JSON schemas -->

## 9. WebSocket Events

<!-- Event types and payload formats -->

## 10. References

## 11. Related Documents

## 12. Status

## 13. Owner

## 14. Last Updated

---

# Template: Database Document

```yaml
---
status: Draft
owner: Data Team
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/08_DATABASE_DESIGN.md
depends_on: ["docs/05_DOMAIN_MODEL.md"]
related_documents: ["docs/09_DATABASE_SCHEMA.md", "docs/10_ENTITY_RELATIONSHIP.md"]
---
```

# {Database Name} - Database Design / Schema

## 1. Purpose

<!-- What data does this database store? Why was this technology chosen? -->

## 2. Scope

<!-- Databases, tables/collections, schemas covered -->

## 3. Technology Selection

| Factor | Decision | Rationale |
|--------|----------|-----------|
| Consistency | | |
| Scalability | | |
| Query Patterns | | |

## 4. Schema Definition

### {Table/Collection Name}

```sql
CREATE TABLE ...
```

## 5. Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| | | | |

## 6. Relationships

<!-- Foreign keys, references to other tables/collections -->

## 7. Partitioning / Sharding

<!-- Strategy and rationale -->

## 8. Retention Policy

<!-- Data retention, archival, deletion rules -->

## 9. Backup Strategy

<!-- Schedule, retention, restore procedure -->

## 10. References

## 11. Related Documents

## 12. Status

## 13. Owner

## 14. Last Updated

---

# Template: Security Document

```yaml
---
status: Draft
owner: Security Team
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/15_SECURITY.md
depends_on: ["docs/13_AUTHENTICATION.md", "docs/14_AUTHORIZATION.md"]
related_documents: ["docs/27_CONFIGURATION.md"]
---
```

# {System Name} - Security Architecture

## 1. Purpose

<!-- Security objectives and scope -->

## 2. Threat Model

<!-- Identified threats and mitigations -->

## 3. Authentication

<!-- Identity verification mechanisms -->

## 4. Authorization

<!-- Access control model (RBAC, ABAC, etc.) -->

## 5. Data Protection

<!-- Encryption at rest and in transit -->

## 6. Network Security

<!-- Segmentation, firewalls, TLS -->

## 7. Secrets Management

<!-- Vault, rotation, access control -->

## 8. Compliance

<!-- GDPR, SOC 2, PCI-DSS, etc. -->

## 9. Incident Response

<!-- Classification and escalation -->

## 10. Vulnerability Management

<!-- Scanning, patching, audits -->

## 11. References

## 12. Related Documents

## 13. Status

## 14. Owner

## 15. Last Updated

---

# Template: Deployment Document

```yaml
---
status: Draft
owner: DevOps Team
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/37_DEPLOYMENT.md
depends_on: ["docs/38_DOCKER.md", "docs/39_KUBERNETES.md"]
related_documents: ["docs/40_CI_CD.md", "docs/48_BACKUP_AND_RECOVERY.md"]
---
```

# {System Name} - Deployment Guide

## 1. Purpose

<!-- Deployment objectives and intended audience -->

## 2. Prerequisites

<!-- Required tools, credentials, access -->

## 3. Environments

| Environment | Purpose | URL | Data |
|-------------|---------|-----|------|
| Development | | | |
| Staging | | | |
| Production | | | |

## 4. Deployment Strategy

<!-- Blue-green, canary, rolling update -->

## 5. Deployment Steps

<!-- Ordered, numbered steps with commands -->

## 6. Configuration

<!-- Environment variables, secrets, configmaps -->

## 7. Health Checks

<!-- Liveness, readiness, startup probes -->

## 8. Rollback Procedure

<!-- Exact steps to revert a deployment -->

## 9. Post-Deployment Verification

<!-- Smoke tests, validation steps -->

## 10. Troubleshooting

<!-- Common issues and resolutions -->

## 11. References

## 12. Related Documents

## 13. Status

## 14. Owner

## 15. Last Updated

---

# Template: ADR (Architecture Decision Record)

```yaml
---
status: Accepted | Superseded | Deprecated
owner: Architecture Team
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/03_ARCHITECTURE_DECISION_RECORDS.md
depends_on: []
related_documents: []
---
```

# ADR-XXXX: {Decision Title}

## Status

Accepted | Superseded by ADR-XXXX | Deprecated

## Context

<!-- What is the issue we are addressing? What constraints exist? -->

## Decision

<!-- What is the chosen solution? What was decided? -->

## Consequences

<!-- What becomes easier or more difficult as a result? -->

## Alternatives Considered

<!-- What other options were evaluated and why were they rejected? -->

## Compliance

<!-- Does this decision affect security, compliance, or regulatory requirements? -->

## References

## Related Documents

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Process & Visualization*

---

# Template: Sprint Report

```yaml
---
status: Approved
owner: Project Manager
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/52_SPRINT_PLANNING.md
depends_on: ["docs/53_PRODUCT_ROADMAP.md"]
related_documents: []
---
```

# Sprint {NN} Report

## 1. Sprint Overview

| Field | Value |
|-------|-------|
| Sprint Number | |
| Start Date | |
| End Date | |
| Velocity Target | |
| Velocity Achieved | |

## 2. Planned vs Completed

| Story | Points | Status |
|-------|--------|--------|
| | | |

## 3. Completed Deliverables

<!-- List deliverables completed this sprint -->

## 4. Carried Over

<!-- Items not completed and reasons -->

## 5. Metrics

| Metric | Value |
|--------|-------|
| Stories Completed | |
| Stories Carried Over | |
| Defects Found | |
| Defects Resolved | |

## 6. Risks and Blockers

<!-- Identified during this sprint -->

## 7. Action Items

<!-- Improvements for next sprint -->

## 8. Demo Notes

<!-- Summary of demo feedback -->

## 9. References

## 10. Related Documents

## 11. Status

## 12. Owner

## 13. Last Updated

---

# Template: Design Document

```yaml
---
status: Draft
owner: Engineering Team
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/44_FOLDER_STRUCTURE.md
depends_on: []
related_documents: []
---
```

# {Feature/Module} - Design Document

## 1. Purpose

<!-- What is being designed and why? -->

## 2. Requirements

<!-- Functional and non-functional requirements addressed -->

## 3. Existing System

<!-- Current behavior and limitations -->

## 4. Proposed Design

### 4.1 High-Level Design

### 4.2 Detailed Design

### 4.3 Data Model

### 4.4 API Changes

### 4.5 Error Handling

### 4.6 Security Considerations

## 5. Alternatives

<!-- Other designs considered and trade-offs -->

## 6. Testing Strategy

<!-- Unit, integration, E2E approach -->

## 7. Migration Plan

<!-- How to migrate existing data/behavior -->

## 8. Rollback Plan

<!-- How to revert if needed -->

## 9. Performance Impact

<!-- Expected performance characteristics -->

## 10. References

## 11. Related Documents

## 12. Status

## 13. Owner

## 14. Last Updated

---

# Template: Module Specification

```yaml
---
status: Draft
owner: Engineering Team
version: 1.0.0
last_updated: YYYY-MM-DD
source_of_truth: docs/44_FOLDER_STRUCTURE.md
depends_on: []
related_documents: []
---
```

# {Module Name} - Module Specification

## 1. Module Overview

<!-- Purpose, scope, placement in system -->

## 2. Module Boundaries

<!-- What is inside vs outside this module -->

## 3. Public Interfaces

<!-- Classes, functions, APIs exposed by this module -->

## 4. Internal Architecture

<!-- Internal structure and patterns -->

## 5. Dependencies

| Dependency | Type | Version | Purpose |
|------------|------|---------|---------|
| | Internal/External | | |

## 6. Configuration

<!-- Module-specific configuration -->

## 7. Error Handling

<!-- Module-level error strategy -->

## 8. Observability

<!-- Logging, metrics, tracing for this module -->

## 9. Testing

<!-- Module test approach -->

## 10. References

## 11. Related Documents

## 12. Status

## 13. Owner

## 14. Last Updated

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Architecture Team*
*Source of Truth: docs/DOCUMENTATION_TEMPLATE.md*
*Depends On: DOCUMENTATION_RULES.md*
*Related Documents: *
*Phase: Foundation*
