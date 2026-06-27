# Implementation Plan: Enterprise Architecture Vision Revision (QX-001A)

**Target Document:** `engineering/enterprise-architecture-vision.md`  
**Source Authority:** Master Development Specification (QX-000) v1.1 Sections 43-60  
**Standards Alignment:** MDS Sections 43-60 governance extensions

---

## Section 1: Document Metadata Update

**Purpose:** Update to reflect MDS 1.1 alignment

**Changes:**
- Document ID: QX-100 remains
- Title: Enterprise Architecture Vision  
- Version: 1.3 (from 1.2)
- Status: REVISION (aligned with MDS Section 1)
- Owner: QuantX AI Enterprise Architecture Board
- Effective Date: 2026-06-27
- Reference: MDS Section 1 (Document Lifecycle), Section 42 (Revision History)

---

## Section 2: Governance Compliance Requirements

**Purpose:** Ensure all architecture decisions reference corresponding MDS sections

**Required MDS Section References:**
- Data Governance → MDS Section 43
- API Governance → MDS Section 44
- Event Governance → MDS Section 46
- Domain Model Governance → MDS Section 49
- Dependency Direction Governance → MDS Section 50
- Error Handling Governance → MDS Section 51
- Observability → MDS Section 47
- Cache Strategy → MDS Section 53
- Feature Flag Strategy → MDS Section 54
- Backup & Disaster Recovery → MDS Sections 55-56

---

## Section 3: Revised Target Data Architecture (MDS Section 43 Alignment)

**Purpose:** Align data architecture with MDS Data Governance Strategy

**Changes to Section 13:**

### Data Governance Integration

The data architecture follows MDS Section 43 Data Governance Strategy:

**Data Ownership and Stewardship (MDS 43.2):**
| Role | Responsibilities | Authority |
|------|-----------------|-----------|
| Data Owner | Define data policies, approve access, ensure compliance | Approve data retention, classify sensitivity |
| Data Steward | Implement policies, monitor quality, manage metadata | Enforce governance rules, resolve data issues |
| Data Custodian | Technical implementation, backup, security controls | Execute operational procedures |

**Data Classification (MDS 43.3):**
| Classification | Description | Handling Requirements | Examples |
|----------------|-------------|----------------------|----------|
| Public | No confidentiality requirements | Unrestricted access | Documentation, public APIs |
| Internal | Limited to organization use | Authenticated access | Internal metrics, non-sensitive configs |
| Confidential | Business-sensitive information | Role-based access, encryption | Trading strategies, user preferences |
| Restricted | Highly sensitive, regulatory impact | Strict access control, audit logging | PII, Sharia-sensitive data, credentials |

**Data Lineage and Metadata Management (MDS 43.5):**
- All data assets maintain lineage tracking from source to destination
- Metadata includes origin timestamp, classification, and ownership
- Master data includes authoritative source designation
- Lineages traceable through transformation pipelines

**Audit Fields (MDS 45.10):**
All tables include audit fields per MDS Section 45:
| Field | Type | Purpose |
|-------|------|---------|
| id | UUID | Surrogate primary key (MDS 45.7) |
| created_at | Timestamp | Creation timestamp |
| created_by | UUID | Creator identity |
| updated_at | Timestamp | Last modification |
| updated_by | UUID | Last modifier identity |
| deleted_at | Timestamp | Soft delete timestamp (MDS 45.11) |
| deleted_by | UUID | Deleter identity |

**Sensitive Data Handling (MDS 43.8):**
- PII scanning on ingestion with automated classification
- Sharia-sensitive data explicitly tagged for compliance
- Masking applied to non-production environments
- Production access requires just-in-time approval

**Cross-references:** MDS Section 43, Section 45 (Database Governance), Section 47 (Observability)

---

## Section 4: Revised Target API Architecture (MDS Section 44 Alignment)

**Purpose:** Align API architecture with MDS API Governance Standards

**Changes to Section 17 (Integration Architecture Vision):**

### API Governance Compliance (MDS 44)

**API Design Principles:**
- Consumer-first: APIs designed for consumer needs
- Consistency: Uniform patterns across all bounded contexts
- Security-by-default: Authentication, authorization at every endpoint
- Observability: Request tracing, metrics, structured logging per MDS 47
- Evolution-friendly: Backward-compatible changes within major versions

**REST Conventions (MDS 44.3):**
- Lowercase paths with kebab-case (e.g., `/api/v1/trading-signals`)
- Plural nouns for collection resources
- Versioning in path: `/api/v{version}/{resource}`

**HTTP Methods (MDS 44.4):**
| Method | Safe | Idempotent | Usage |
|--------|------|------------|-------|
| GET | Yes | Yes | Retrieve resource or collection |
| POST | No | No | Create new resource |
| PUT | No | Yes | Replace resource entirely |
| PATCH | No | No | Partial resource update |
| DELETE | No | Yes | Remove resource |

**Versioning Policy (MDS 44.5):**
- Major versions (`v1`, `v2`) in path for breaking changes
- Minor features added within major version without incrementing
- Deprecated versions receive minimum 6-month notice
- Deprecation announced via response headers

**Error Response Format (MDS 44.7):**
Standardized error envelope per MDS Section 44:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [{"field": "email", "issue": "Invalid email format"}],
    "correlationId": "txn_abc123def456",
    "timestamp": "2026-06-27T14:57:08Z"
  }
}
```

**OpenAPI Requirements (MDS 44.10):**
- Specification stored at `docs/api/openapi.yaml` per bounded context
- CI validates specification against implementation
- Client SDK generation from specification

**Cross-references:** MDS Section 44, Section 47 (Observability), Section 51 (Error Handling), Section 48 (Testing)

---

## Section 5: Revised Target Event Architecture (MDS Section 46 Alignment)

**Purpose:** Align event architecture with MDS Event Governance Standards

**New Section:** Add after Section 17 Integration Architecture Vision

### Event Governance Compliance (MDS 46)

**Event Naming (MDS 46.1):**
- Past-tense verbs indicating completed action
- kebab-case formatting: `{domain}.{verb}.{noun}` (e.g., `market-signal.created`)

**Event Versioning (MDS 46.2):**
- Major version for breaking schema changes in event envelope
- Version included in event envelope
- Consumers register for specific event versions

**Immutable Events (MDS 46.3):**
- No modification after publishing
- Corrections handled via compensating events
- Event store optimized for append-only

**Payload Standards (MDS 46.4):**
- JSON as default serialization format
- Mandatory envelope fields: `eventId`, `eventType`, `timestamp`, `version`, `source`
- No secrets in event payloads

**Event Publishing (MDS 46.6):**
- Asynchronous publishing from bounded context
- At-least-once delivery guarantee
- Publish after transaction commit
- Failed events routed to DLQ

**Event Consumption (MDS 46.7-46.9):**
- Idempotent processing required
- Acknowledgement after successful processing
- Exponential backoff retry (1s initial, 60s max, 5 attempts max)
- Dead letter queue retention 30 days

**Correlation IDs (MDS 46.11):**
- Correlation ID propagated across all boundaries
- Causation ID for child operations
- Full trace reconstruction enabled

**Cross-references:** MDS Section 46, Section 43 (Data), Section 47 (Observability), Section 51 (Error Handling)

---

## Section 6: Revised Target Domain Model (MDS Section 49 Alignment)

**Purpose:** Align domain model with MDS Domain Model Governance

**Changes to Section 26 (Bounded Context Strategy):**

### Domain Model Governance Compliance (MDS 49)

**Aggregate Rules (MDS 49.1):**
- Single Aggregate Root per aggregate
- Invariants enforced within aggregate boundary
- Cross-context references only by identity
- Aggregate boundaries align with transaction boundaries

**Aggregate Root Responsibilities (MDS 49.2):**
- Invariant maintenance within boundary
- Creation and modification control
- Domain event publishing on state change (MDS 46)
- Stable identity across state changes

**Domain Services (MDS 49.6):**
- Cross-aggregate logic placement
- Stateless operation only
- Ubiquitous language terminology
- Domain layer location only

**Repositories (MDS 49.7):**
- Domain-layer interfaces only
- Infrastructure-layer implementations
- Aggregate Root retrieval only
- Identity-based retrieval operations

**Domain Events (MDS 49.9):**
- Published by Aggregate Root only
- Immutable after publication
- Naming per MDS Section 46
- Minimal payload with essential data only

**Invariants (MDS 49.10-49.11):**
- Enforced within Aggregate Root
- Cross-aggregate via domain services
- Compensating transactions for distributed invariants

**Business Rule Ownership (MDS 49.12):**
| Rule Type | Owner | Responsibility |
|-----------|-------|----------------|
| Invariant | Domain Architect | Domain-level enforcement |
| Validation | Domain/Application | Boundary validation |
| External Policy | Compliance | Regulatory rules |
| Integration | Domain Architect | Cross-context rules |

**Cross-references:** MDS Section 49, Section 46 (Event), Section 50 (Dependency), Section 45 (Database)

---

## Section 7: Revised Dependency Direction (MDS Section 50 Alignment)

**Purpose:** Ensure Clean Architecture dependency rules with MDS compliance

**New Section:** Add after Section 12 (Target Application Architecture)

### Dependency Direction Governance (MDS 50)

**Dependency Hierarchy (MDS 50.1):**
```
Presentation Layer → Application Layer → Domain Layer → Infrastructure Layer
```
Dependencies point inward only. Outer layers may depend on inner layers through interfaces.

**Layer Responsibilities (MDS 50.2):**
| Layer | Depends On | Responsibility |
|-------|------------|----------------|
| Domain | None | Business logic, invariants |
| Application | Domain | Use cases, orchestration |
| Infrastructure | Application/Domain | External integrations |
| Presentation | Application | User interface, transport |

**Forbidden Patterns (MDS 50.3):**
- Domain importing from outer layers
- Application importing Infrastructure/Presentation bypassing interfaces
- Presentation bypassing Application layer
- Cross-context domain sharing
- Business logic in outer layers

**Circular Dependency Prevention (MDS 50.4):**
- Module-level lint rules block circular imports
- Package-level CI failure on cycles detected
- Bounded-context interface contracts
- Dependency inversion through interfaces

**Cross-references:** MDS Section 50, Section 7 (Architecture Principles), Section 6 (Engineering Principles)

---

## Section 8: Revised Error Handling (MDS Section 51 Alignment)

**Purpose:** Align error handling with MDS Error Handling Governance

**New Section:** Add after Section 22 (Observability Vision)

### Error Handling Governance (MDS 51)

**Exception Hierarchy (MDS 51.1):**
- QuantXException (base)
  - DomainException: Business rule violations
  - ValidationException: Boundary validation failures
  - InfrastructureException: External system failures
  - ApplicationException: Use case failures

**Domain Exceptions (MDS 51.2):**
- Business rule violations raised as exceptions
- No internal implementation detail exposure
- User-friendly messages for known violations
- Exception codes for programmatic handling

**Infrastructure Exceptions (MDS 51.4):**
- Caught at hexagonal adapter boundaries
- Logged with full context per MDS 47
- Generic user response returned
- Retry candidates identified

**Application Exceptions (MDS 51.5):**
- Use case failures with correlation ID
- Structured logging per MDS 47 Observability
- HTTP status mapping defined
- Recovery guidance in error response

**Logging Rules (MDS 51.6):**
- Logging at catch point, not throw point
- Production secret exclusion enforced
- Structured logging per MDS Section 47
- Full stack trace in internal logs only

**User-Facing Errors (MDS 51.7):**
- Standardized envelope per MDS 44 API Governance
- Actionable language without internal details
- Error codes for consumer handling
- Correlation ID for support reference

**Cross-references:** MDS Section 51, Section 8 (Security), Section 47 (Observability), Section 44 (API)

---

## Section 9: Revised Observability (MDS Section 47 Alignment)

**Purpose:** Align observability with MDS Observability Governance Strategy

**Changes to Section 22 (Observability Vision):**

### Observability Governance Compliance (MDS 47)

**Structured Logging (MDS 47.1-47.3):**
- JSON format for all log entries
- Mandatory fields: timestamp, severity, service, environment, traceId, spanId, message, correlationId
- Log levels: TRACE, DEBUG, INFO, WARN, ERROR, FATAL

**Metrics (MDS 47.6):**
- RED metrics: Rate, Errors, Duration for request-driven services
- USE metrics: Utilization, Saturation, Errors for resource-driven services
- Business metrics tracked alongside system metrics
- Cardinality control enforced on labels

**SLIs and SLOs (MDS 47.7-47.8):**
| SLI | Target | Measurement Window |
|-----|--------|-------------------|
| Availability | ≥99.9% | 30-day rolling |
| Latency (p95) | <500ms | Hourly |
| Error Rate | ≤0.1% | Hourly |
| Freshness | ≤30s | Event-driven metrics |

**Alerting (MDS 47.9):**
| Severity | Response Time | Escalation | Runbook |
|----------|--------------|------------|---------|
| P1 | 15 minutes | 24/7 on-call | Page/SMS |
| P2 | 1 hour | Business hours | Slack/Email |
| P3 | 4 hours | Team lead | Ticket |
| P4 | 24 hours | Next business day | Ticket |

**Distributed Tracing (MDS 47.5):**
- OpenTelemetry SDK for language-native instrumentation
- Semantic conventions for span attributes
- End-to-end span coverage across services
- Trace sampling configured per environment

**Retention Policy (MDS 47.11):**
| Data Type | Hot Storage | Cold Storage |
|-----------|-------------|--------------|
| Logs | 90 days | 2 years |
| Metrics | 13 months | N/A |
| Traces | 30 days | N/A |
| Audit | 7 years | 7 years |

**Cross-references:** MDS Section 47, Section 8 (Security), Section 26 (Quality Gates)

---

## Section 10: Revised Cache Strategy (MDS Section 53 Alignment)

**Purpose:** Align cache management with MDS Cache Management Strategy

**Changes to Section 19 (Scalability Strategy):**

### Cache Management Strategy (MDS 53)

**Cache Hierarchy (MDS 53.2):**
- L1: Application/local memory cache
- L2: Distributed Redis cache
- L3: CDN for static assets and API responses

**Cache Key Design (MDS 53.3):**
- Namespaced by service and resource
- Deterministic based on input parameters
- Collision-resistant with hash functions
- Includes version segment for invalidation

**Invalidation Policies (MDS 53.4):**
- TTL-based expiration as safety net
- Event-driven invalidation on data change
- Write-through preferred over write-behind
- Cache-aside pattern for read-heavy data

**Cache Warming (MDS 53.5):**
- Cache warming for predictable loads
- Gradual warming to prevent overload
- Preloading schedule aligned with load patterns

**Consistency and Security (MDS 53.6-53.7):**
- Eventual consistency acceptable with defined staleness maximum
- Cache stampede prevention through staggered TTL
- No sensitive data in cache without encryption
- Limited cache key exposure to users

**Observability (MDS 53.8):**
- Hit ratio tracking per cache layer
- Miss ratio and eviction rate monitoring
- Staleness age tracking
- SLO for cache availability (99.9%)

**Cross-references:** MDS Section 53, Section 47 (Observability), Section 43 (Data)

---

## Section 11: Revised Feature Flag Strategy (MDS Section 54 Alignment)

**Purpose:** Align feature flags with MDS Feature Flag Governance

**Changes to Section 18 (Deployment Vision):**

### Feature Flag Governance (MDS 54)

**Feature Flag Types (MDS 54.2):**
- Release flags: New feature rollout
- Operational flags: Runtime configuration
- Experiment flags: A/B testing variants
- Permission flags: Entitlement management

**Feature Flag Lifecycle (MDS 54.3):**
- Creation → Active → Cleanup
- Maximum 90-day lifetime for temporary flags
- Removal required before permanent state
- Flag removal tracked in technical debt register

**Flag Naming (MDS 54.4):**
- Format: `{domain}.{feature}.{variant}` (e.g., `trading.sharia.enforcement`)
- Environment prefix for environment-specific flags
- Consistent naming across all services

**Evaluation Rules (MDS 54.5):**
- Server-side evaluation required for critical flags
- Fallback values for evaluation failures
- Evaluation latency < 1ms
- Sharia Mode gating for compliance features

**Targeting Rules (MDS 54.6):**
- Percentage rollout for gradual enablement
- User segment targeting for beta users
- Environment gating for staging testing

**Audit and Compliance (MDS 54.7):**
- All flag changes logged with user and timestamp
- Flag state included in audit trail
- Compliance review for business-critical flags
- Quarterly flag usage review

**Cross-references:** MDS Section 54, Section 25 (Definition of Done), Section 30 (Compliance)

---

## Section 12: Revised Backup & Disaster Recovery (MDS Sections 55-56 Alignment)

**Purpose:** Align B&R with MDS Backup and Disaster Recovery Strategies

**Changes to Sections 21 (Disaster Recovery Vision) and Section 19 (Scalability):**

### Backup and Restore Strategy (MDS 55)

**Objectives:**
- Data durability against system failures
- Recovery capability within RTO constraints
- Business continuity support during outages
- Compliance archive for regulated data

**Recovery Objectives (MDS 55.5-56.6):**

| System Tier | RTO | RPO |
|-------------|-----|-----|
| Tier 1 — Trading and risk (Sharia Mode active) | ≤ 1 hour | ≤ 5 minutes |
| Tier 2 — Market intelligence and signals | ≤ 4 hours | ≤ 15 minutes |
| Tier 3 — Reporting, analytics, non-critical | ≤ 24 hours | ≤ 4 hours |

**Backup Classification (MDS 55.3):**
- Full: Complete database snapshot
- Incremental: Changes since last full/incremental
- Transaction log: Continuous log backups

**Backup Frequency (MDS 55.4):**
- Daily full backups retained 30 days
- Hourly incremental backups retained 30 days
- 7-year compliance archive for regulated data
- Offsite replication within 4 hours

**Restore Procedures (MDS 55.6):**
- RTO-aligned restore procedures documented
- Automated restore testing monthly
- Runbooks maintained for each restore scenario
- Point-in-time recovery available

### Disaster Recovery Strategy (MDS 56)

**Disaster Classification:**
- Level 1: Single service degradation (< 4 hours)
- Level 2: Bounded context failure (< 24 hours)
- Level 3: Regional infrastructure failure (< 72 hours)
- Level 4: Complete platform failure (< 7 days)

**Recovery Strategies:**
- Tier 1: Warm standby in secondary region
- Tier 2: Pilot light with automated activation
- Tier 3: Backup restore procedures
- Multi-region active-active for critical paths

**Failover and Failback (MDS 56.8-56.9):**
- Automated failover where RTO permits
- Manual approval required for Tier 1
- Failback after root cause resolution
- Failback testing quarterly

**Cross-references:** MDS Section 55, Section 56, Section 43 (Data), Section 45 (Database)

---

## Section 13: Integration Checklist

**Purpose:** Verify all MDS 43-60 sections properly referenced

### Verification Matrix

| Governance Area | MDS Section | Status | Evidence Location |
|-----------------|-------------|--------|-------------------|
| Data Governance | Section 43 | ✓ | Section 3, 13 |
| API Governance | Section 44 | ✓ | Section 17, 4 |
| Event Governance | Section 46 | ✓ | New Section 5 |
| Domain Model Governance | Section 49 | ✓ | Section 26 |
| Dependency Direction | Section 50 | ✓ | New Section 7 |
| Error Handling | Section 51 | ✓ | New Section 8 |
| Observability | Section 47 | ✓ | Section 22 |
| Cache Strategy | Section 53 | ✓ | Section 19 |
| Feature Flag Strategy | Section 54 | ✓ | Section 18 |
| Backup & DR | Sections 55-56 | ✓ | Sections 21, 19 |

---

## Section 14: Acceptance Criteria

**Purpose:** Define completion requirements per MDS Section 7

### Criteria

- [ ] All architecture decisions reference corresponding MDS section (43-60)
- [ ] Clean Architecture dependency rules enforced (no outer-to-inner dependencies)
- [ ] DDD patterns implemented with proper aggregate boundaries
- [ ] Data governance roles defined (Owner, Steward, Custodian)
- [ ] API governance standards applied (versioning, error format, OpenAPI)
- [ ] Event governance followed (naming, versioning, immutability)
- [ ] Observability standards implemented (structured logging, SLIs/SLOs)
- [ ] Cache strategy defined (hierarchy, invalidation, warming)
- [ ] Feature flag lifecycle governed (creation to cleanup)
- [ ] Backup/DR objectives aligned with RTO/RPO targets
- [ ] Error handling hierarchy extends QuantXException base
- [ ] No implementation details (technology-aware, not technology-specific)
- [ ] All cross-references to MDS use exact section headings

---

## Section 15: Revision Summary

**Purpose:** Document changes for Revision History

**Changes to Apply:**
1. Update Document Metadata to v1.3 with REVISION status
2. Add Data Governance subsection to Section 13 (Data Architecture)
3. Add API Governance subsection to Section 17 (Integration Architecture)
4. Add Event Governance as Section 18 (after Integration Architecture)
5. Add Domain Model Governance to Section 26 (Bounded Context Strategy)
6. Add Dependency Direction Governance as Section 13 (after Application Architecture)
7. Add Error Handling Governance as Section 23 (after Observability Vision)
8. Expand Section 22 (Observability Vision) with MDS 47 compliance
9. Expand Section 19 (Scalability Strategy) with MDS 53 cache strategy
10. Expand Section 18 (Deployment Vision) with MDS 54 feature flags
11. Expand Sections 21 (Disaster Recovery) and 13 (Data Architecture) with MDS 55-56

---

## Section 16: References

**Purpose:** Cite governing standards

- Master Development Specification (QX-000) v1.1 - QuantX AI Enterprise Architecture Board
- ISO/IEC 8000 - Data Quality (MDS Section 43)
- ISO/IEC 11179 - Metadata Registries (MDS Section 43)
- OpenAPI 3.0.3 - API Description Format (MDS Section 44)
- CloudEvents 1.0 - Event Specification (MDS Section 46)
- OpenTelemetry 1.0 - Observability Specification (MDS Section 47)
- ISO/IEC 9075 (SQL:2016) - Database Language (MDS Section 45)
- Redis Documentation - Cache Strategy (MDS Section 53)

---

# Standards Mapping

| Standard | Influence on Document | Specific Sections |
|----------|----------------------|-------------------|
| ISO/IEC 8000 | Data quality dimensions | 3, 13 |
| ISO/IEC 11179 | Metadata standardization | 3, 13 |
| OpenAPI 3.0.3 | API governance | 17, 4 |
| CloudEvents 1.0 | Event specification | 5, 26 |
| OpenTelemetry 1.0 | Observability | 22 |
| Prometheus Format | Metrics collection | 22 |
| SQL:2016 | Database constraints | 13, 3 |
| ISO/IEC 38500 | IT Governance | 3, 17 |

# Quality Gates

- [ ] All MDS sections 43-60 referenced in architecture decisions
- [ ] Clean Architecture and DDD remain authoritative
- [ ] No architectural redesign - only synchronization
- [ ] All cross-cutting concerns aligned to MDS governance
- [ ] Document follows MDS Section 18 Document Lifecycle format
- [ ] Revision history updated with proper version increment