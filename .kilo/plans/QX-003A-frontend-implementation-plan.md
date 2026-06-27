# Implementation Plan: Frontend Implementation (QX-003A)

**Target Document:** `apps/quantx-web/` (Frontend Web Application)  
**Source Authority:** Master Development Specification v1.1 Sections 44, 47, 51, 53, 54, 58, 59, 26  
**Standards Alignment:** MDS API Governance, Observability, Error Handling, Cache Management, Feature Flag, Internationalization, Performance Engineering

---

## Section 1: Document Metadata

- **Document ID:** QX-003A
- **Title:** Frontend Implementation Plan
- **Version:** 1.0
- **Status:** IMPLEMENTATION
- **Owner:** QuantX AI Enterprise Architecture Board
- **Effective Date:** 2026-06-27
- **Reference:** MDS Section 1 (Document Lifecycle), Section 42 (Revision History)

---

## Section 2: Frontend Milestones

| Milestone | MDS Reference | Target | Deliverables |
|-----------|---------------|--------|--------------|
| M1 | Section 44 | API Integration | API client, OpenAPI contract consumption, error handling |
| M2 | Section 47 | Observability | Frontend logging, error tracking, user metrics, frontend SLOs |
| M3 | Section 51 | Error Handling | Error boundaries, user-facing error display, correlation tracking |
| M4 | Section 53 | Cache Strategy | Client-side cache, cache invalidation, offline strategies |
| M5 | Section 54 | Feature Flags | Flag client, targeting rules, Sharia Mode gating |
| M6 | Section 58 | Internationalization | i18n framework, RTL support, Arabic localization |
| M7 | Section 59 | Performance | Core Web Vitals, bundle budgets, lazy loading, performance monitoring |
| M8 | Section 26 | Quality Gates | Accessibility compliance, lint rules, testing standards |

---

## Section 3: Frontend Deliverables

### 3.1 API Governance Compliance (MDS Section 44)

**API Client Layer:**
- REST client consuming OpenAPI 3.0 specification from `docs/api/openapi.yaml`
- Standardized error envelope handling per MDS 44.7
- Request/response interceptors for authentication token injection
- Idempotency key support for non-idempotent operations per MDS 44.8
- Rate limit handling with backoff and retry logic per MDS 44.9
- Versioned API paths (`/api/v1/{resource}`) following MDS 44.5
- Pagination, filtering, and sorting support per MDS 44.9

**API Integration Rules:**
- No direct API calls outside client layer
- Environment-based API endpoint configuration
- API response typing from OpenAPI specification
- Request retry with exponential backoff for network failures
- Circuit breaker pattern for failing endpoints

### 3.2 Observability Deliverables (MDS Section 47)

**Frontend Logging:**
- Structured logging for user actions and system events
- Correlation ID propagation from API responses to frontend logs
- Log levels: ERROR, WARN, INFO for client-side events
- No sensitive data in client-side logs
- Integration with OpenTelemetry via JavaScript SDK

**Frontend Metrics:**
- RED metrics: Request rate, Error rate, Duration for API calls
- User interaction metrics for business tracking
- Web Vitals collection (LCP, FID, CLS) per MDS 59.10
- Performance marks and measures for user experience
- Error boundary metrics and unhandled exception tracking
- Navigation timing and resource timing metrics

**Tracing:**
- OpenTelemetry browser SDK instrumentation
- Span correlation across frontend-backend boundary
- Trace sampling configured per environment (100% dev, 10% prod)
- Trace context propagation via HTTP headers

### 3.3 Error Handling Deliverables (MDS Section 51)

**Error Boundary Strategy:**
- Global error boundaries for component-level failures
- API error handling with standardized envelope parsing
- User-friendly error messages without internal details
- Error codes for programmatic handling
- Correlation ID extraction and display for support reference

**Frontend Error Handling:**
- QuantXException-derived error handling in client code
- Validation errors displayed inline with field-level detail
- Network error handling with offline detection
- Graceful degradation for non-critical failures
- Error logging to observability pipeline

### 3.4 Cache Management Deliverables (MDS Section 53)

**Client-Side Cache Strategy:**
- React Query or SWR for server state caching
- L1 cache in browser memory for active session
- Cache key namespacing per MDS 53.3
- TTL-based expiration for all cached data
- Cache invalidation on mutation (write-through pattern)
- Offline cache support for critical read operations

**Cache Security:**
- No sensitive data in browser cache
- Cache size limits enforced
- Cache encryption for confidential data
- Session-based cache isolation

### 3.5 Feature Flag Deliverables (MDS Section 54)

**Flag Client Implementation:**
- LaunchDarkly, GrowthBook, or custom flag provider integration
- Flag types: release, operational, experiment, permission
- Flag naming: `{domain}.{feature}.{variant}` per MDS 54.4
- Server-side flag evaluation for critical features
- Client-side flag evaluation with server fallback
- Sharia Mode gating for compliance features

**Flag Lifecycle Management:**
- Flag initialization on application start
- Flag change listener for runtime updates
- Flag persistence for offline scenarios
- Audit logging of flag evaluations (non-personal)

### 3.6 Internationalization Deliverables (MDS Section 58)

**i18n Framework:**
- Next.js i18n routing support
- BCP 47 locale codes (`en-US`, `ar-SA`)
- Arabic-first RTL support for Sharia Mode
- Externalized strings in JSON resource files
- Translation management system integration
- Currency and date formatting per locale

**Language Support:**
- English (Primary) - Full interface support
- Arabic (Mandatory) - Full Sharia Mode support with RTL layout
- Fallback chain to English for missing translations

### 3.7 Performance Engineering Deliverables (MDS Section 59)

**Frontend Performance Budget:**
- Core Web Vitals targets: LCP < 2.5s, FID < 100ms, CLS < 0.1
- Bundle size budget per route (e.g., 250KB limit)
- Lazy loading for non-critical components
- Code splitting per bounded context
- Image optimization with Next.js Image component
- Performance monitoring in staging environment

---

## Section 4: Acceptance Criteria

### 4.1 API Governance Compliance (MDS Section 44)
- [ ] All API calls use versioned `/api/v{version}/` paths
- [ ] Error responses follow standardized envelope format
- [ ] OpenAPI specification consumed and types generated
- [ ] Rate limiting handled gracefully with retry logic
- [ ] Idempotency keys passed for write operations

### 4.2 Observability Compliance (MDS Section 47)
- [ ] Structured logging for all user actions and errors
- [ ] RED metrics collected and sent to monitoring backend
- [ ] OpenTelemetry tracing spans created for API calls
- [ ] Web Vitals collected and reported
- [ ] Correlation IDs propagated from backend to frontend

### 4.3 Error Handling Compliance (MDS Section 51)
- [ ] Error boundaries wrap all route segments
- [ ] User-facing errors use standardized format without internal details
- [ ] Validation errors display field-level details
- [ ] Correlation ID displayed in error UI for support
- [ ] All errors logged to observability pipeline

### 4.4 Cache Management Compliance (MDS Section 53)
- [ ] Cache keys follow namespaced format per MDS 53.3
- [ ] TTL configured for all cached queries
- [ ] Cache invalidation triggered on data mutations
- [ ] Cache hit ratio monitored with 95% target
- [ ] Offline cache support for critical read paths

### 4.5 Feature Flag Compliance (MDS Section 54)
- [ ] Flag client initialized on app startup
- [ ] Flag naming follows `{domain}.{feature}.{variant}` pattern
- [ ] Sharia Mode flags gated appropriately for compliance features
- [ ] Flag evaluations logged (non-personal) for audit
- [ ] Temporary flags have removal dates documented

### 4.6 Internationalization Compliance (MDS Section 58)
- [ ] Arabic RTL support implemented with proper layout
- [ ] Locale detection and preference persistence
- [ ] All user-facing strings externalized to resource files
- [ ] Number/date/currency formatting per locale
- [ ] English fallback for missing translations

### 4.7 Performance Compliance (MDS Section 59)
- [ ] Core Web Vitals targets achieved (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- [ ] Bundle budgets enforced per route
- [ ] Lazy loading implemented for all non-critical components
- [ ] Performance testing integrated in CI/CD pipeline
- [ ] Performance regression detection enabled

### 4.8 Quality Gates Compliance (MDS Section 26)
- [ ] Accessibility pass WCAG 2.1 AA for all components
- [ ] Lint pass with no errors or warnings
- [ ] Type-check pass in strict mode
- [ ] Unit tests passing with coverage threshold (80%)
- [ ] End-to-end tests for critical user journeys

---

## Section 5: Verification Steps

### 5.1 API Governance Verification (MDS Section 44)
```bash
# Verify OpenAPI types generated
npm run openapi:generate

# Verify REST conventions in API client
npm run lint:api-client

# Verify error envelope handling
npm run test:api-errors

# Verify rate limit handling
npm run test:rate-limits
```

### 5.2 Observability Verification (MDS Section 47)
```bash
# Verify structured logging format
npm run test:logging-format

# Verify metrics emission
npm run test:metrics-emission

# Verify tracing coverage
npm run trace:coverage

# Verify Web Vitals collection
npm run test:web-vitals
```

### 5.3 Error Handling Verification (MDS Section 51)
```bash
# Verify error boundary coverage
npm run check:error-boundaries

# Verify error envelope format
npm run test:error-display

# Verify correlation ID propagation
npm run test:correlation-flow

# Verify validation error handling
npm run test:validation-errors
```

### 5.4 Cache Management Verification (MDS Section 53)
```bash
# Verify cache key format
npm run lint:cache-keys

# Verify TTL configuration
npm run check:cache-ttl

# Verify cache invalidation on mutations
npm run test:cache-invalidation

# Verify offline cache behavior
npm run test:offline-cache
```

### 5.5 Feature Flag Verification (MDS Section 54)
```bash
# Verify flag naming convention
npm run lint:flags

# Verify flag targeting rules
npm run test:flag-targeting

# Verify Sharia Mode flag gating
npm run test:sharia-flags

# Verify fallback values
npm run test:flag-fallback
```

### 5.6 Internationalization Verification (MDS Section 58)
```bash
# Verify locale detection
npm run test:locale-detection

# Verify RTL layout for Arabic
npm run test:rtl-layout

# Verify string externalization
npm run check:externalized-strings

# Verify fallback chain
npm run test:i18n-fallback
```

### 5.7 Performance Verification (MDS Section 59)
```bash
# Verify Core Web Vitals targets
npm run metrics:web-vitals

# Verify bundle budgets
npm run metrics:bundle-size

# Verify lazy loading
npm run check:lazy-loading

# Verify performance in staging
npm run test:perf-staging
```

---

## Section 6: Repository Structure

```
apps/quantx-web/
├── src/
│   ├── presentation/                # Next.js pages and components
│   │   ├── pages/                 # Route pages with error boundaries
│   │   ├── components/            # Reusable UI components
│   │   │   └── common/            # Pattern library components
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── layouts/               # Page layouts (RTL-aware)
│   │   └── styles/                # Global styles, Tailwind config
│   ├── application/                 # Application services
│   │   ├── api/                   # API client layer
│   │   │   ├── client.ts          # Base API client
│   │   │   └── endpoints/         # Generated endpoint clients
│   │   └── services/              # Client-side services
│   ├── shared/                      # Shared utilities
│   │   ├── kernel/                # Error types, utilities
│   │   ├── i18n/                # Internationalization utilities
│   │   ├── cache/                 # Cache configuration and hooks
│   │   ├── flags/                 # Feature flag client
│   │   └── observability/         # Logging, metrics, tracing
│   ├── infrastructure/              # External integrations
│   │   ├── telemetry/             # OpenTelemetry browser setup
│   │   └── storage/               # LocalStorage, IndexedDB wrappers
│   └── features/                    # Feature-based modules
│       ├── market-intelligence/
│       ├── trading-signals/
│       ├── portfolio/
│       ├── risk-management/
│       └── sharia-compliance/
├── public/                          # Static assets
├── tests/                           # Frontend tests
│   ├── unit/
│   ├── integration/
│   └── e2e/                         # Playwright/Cypress tests
├── docs/
│   └── api/
│       └── openapi.yaml             # OpenAPI spec from backend
├── next.config.js                     # Next.js configuration
├── tailwind.config.js                 # Tailwind with RTL support
├── tsconfig.json                      # TypeScript strict mode
└── package.json
```

---

## Section 7: Frontend Quality Gates

### 7.1 Mandatory Quality Gates (MDS Section 26)

| Gate | MDS Reference | Threshold | Tool |
|------|---------------|-----------|------|
| G1 | Section 59.10 | Core Web Vitals pass | Lighthouse CI |
| G2 | Section 26 | WCAG 2.1 AA compliance | axe-core |
| G3 | Section 48.1 | Unit coverage ≥80% | Jest coverage |
| G4 | Section 47.7 | P95 latency <500ms | Load test (frontend) |
| G5 | Section 44.7 | Error envelope compliance | Jest tests |
| G6 | Section 58 | i18n locale coverage | i18n linter |
| G7 | Section 51 | Error handling coverage | Jest tests |
| G8 | Section 53 | Cache hit ratio ≥95% | Browser metrics |
| G9 | Section 54 | Flag audit logging | Jest tests |

### 7.2 Frontend-Specific Quality Gates

- [ ] All pages pass Lighthouse accessibility audit (WCAG 2.1 AA)
- [ ] Bundle size under 250KB per route
- [ ] First contentful paint < 1.5 seconds
- [ ] Largest contentful paint < 2.5 seconds
- [ ] CLS score < 0.1 for all pages
- [ ] Error boundaries cover 100% of component tree
- [ ] Cache interceptors handle offline gracefully

---

## Section 8: Mapping to MDS Governance Sections

| Frontend Area | MDS Section | Key Requirements |
|---------------|-------------|------------------|
| **API Integration** | 44 | REST conventions, versioning, error format, OpenAPI |
| **Observability** | 47 | Structured logging, metrics, tracing, alerting |
| **Error Handling** | 51 | Exception hierarchy, user-facing format, logging |
| **Cache Strategy** | 53 | Hierarchy, keys, invalidation, observability |
| **Feature Flags** | 54 | Types, lifecycle, targeting, audit |
| **Internationalization** | 58 | Language tiers, RTL, locale management |
| **Performance** | 59 | Web Vitals targets, caching, incident response |
| **Accessibility** | 26 | WCAG 2.1 AA compliance for all components |

---

## Section 9: Frontend Quality Gates Match MDS

### 9.1 Accessibility Consistency (MDS Section 26)
- WCAG 2.1 AA compliance mandatory for all components
- Color contrast ratios ≥ 4.5:1 for normal text
- Keyboard navigation support for all interactive elements
- ARIA attributes properly implemented
- Screen reader compatibility tested

### 9.2 Quality Gate Alignment
Frontend quality gates directly map to MDS Section 26 definitions:
- Coverage thresholds: Unit test coverage ≥ 80%, Integration test coverage ≥ 60%
- Lint pass with no errors or warnings (ESLint + accessibility plugin)
- Typecheck pass in strict mode
- No critical or high severity vulnerabilities in dependency scan
- Performance benchmark pass (Core Web Vitals targets)
- Accessibility pass for frontend components (WCAG 2.1 AA)

---

## Section 10: Backup Implications

### 10.1 Client-Side Data Backup
- User preferences and settings backed up to backend
- Auth tokens and session state handled via secure HTTP-only cookies
- Cached data is ephemeral; no persistent backup required
- Offline data synchronized on reconnection
- LocalStorage cleared on new version deployments

### 10.2 Offline and PWA Considerations
- Service worker caches static assets for offline availability
- IndexedDB used for temporary offline data storage
- Data conflict resolution on reconnection
- Progressive enhancement for core functionality

---

## Section 11: Cross-References

- **MDS Section 44 (API Governance):** REST conventions, versioning, error format, OpenAPI
- **MDS Section 47 (Observability):** Structured logging, metrics, distributed tracing
- **MDS Section 51 (Error Handling):** Exception hierarchy, error responses
- **MDS Section 53 (Cache Management):** Cache hierarchy, key design, invalidation
- **MDS Section 54 (Feature Flags):** Flag types, lifecycle, targeting
- **MDS Section 58 (Internationalization):** Language support, RTL layout
- **MDS Section 59 (Performance Engineering):** Core Web Vitals, performance budgets
- **MDS Section 26 (Quality Gates):** Accessibility, lint, test coverage thresholds