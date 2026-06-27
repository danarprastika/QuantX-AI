# QuantX Platform Backend

Modular Monolith Backend implementing Clean Architecture with DDD bounded contexts.

## Overview

This repository implements the QuantX AI backend following:
- Clean Architecture (MDS Section 7)
- Domain-Driven Design (MDS Section 49)
- Data Governance (MDS Section 43)
- API Governance (MDS Section 44)
- Event Governance (MDS Section 46)
- Observability Governance (MDS Section 47)
- Testing Governance (MDS Section 48)
- Dependency Direction Governance (MDS Section 50)
- Error Handling Governance (MDS Section 51)
- Cache Management (MDS Section 53)
- Feature Flag Governance (MDS Section 54)
- Backup & DR (MDS Sections 55-56)

## Quick Start

```bash
# Install dependencies
npm install

# Generate Prisma client
npm run prisma:generate

# Run database migrations
npm run prisma:migrate

# Start development server
npm run start:dev
```

## Architecture

The codebase follows Clean Architecture with four layers:

```
Presentation → Application → Domain → Infrastructure
```

See [MDS Section 50](https://kilo.ai/docs/mds#50-dependency-direction-governance) for dependency rules.

## Bounded Contexts

| Context | Description | MDS Reference |
|---------|-------------|---------------|
| market-intelligence | Market data processing and signals | Section 43, 49 |
| trading-signals | Signal generation and analytics | Section 46, 49 |
| portfolio | Portfolio optimization and management | Section 43, 49 |
| risk-management | Risk assessment and compliance monitoring | Section 43, 49 |
| sharia-compliance | Sharia compliance engine | Section 43, 49 |

## Compliance

### Data Classification (MDS 43.3)
- **Restricted:** PII, Sharia-sensitive data, credentials
- **Confidential:** Trading strategies, user preferences
- **Internal:** Internal metrics, non-sensitive configs
- **Public:** Documentation, public APIs

### Sharia Mode
The platform supports dual operating modes. See [MDS Section 54](https://kilo.ai/docs/mds#54-feature-flag-governance) for flag implementation.

## Quality Gates

- Unit coverage: ≥80% (MDS Section 48.1)
- Integration coverage: ≥60% (MDS Section 48.2)
- Cache hit ratio: ≥95% (MDS Section 53.8)
- P95 latency: <500ms (MDS Section 47.7)
- Error rate: ≤0.1% (MDS Section 47.8)