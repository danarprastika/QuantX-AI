# QuantX AI - Versioning

## Overview

This document defines the versioning strategy for QuantX AI, including semantic versioning, API versioning, database migrations, and backward compatibility policies.

## Versioning Standards

### Semantic Versioning
Format: MAJOR.MINOR.PATCH (e.g., 1.2.3)

| Component | When to Increment |
|-----------|-------------------|
| MAJOR | Breaking changes, incompatible API changes |
| MINOR | New features, backward-compatible changes |
| PATCH | Bug fixes, backward-compatible changes |

### Pre-release Suffixes
- `1.0.0-alpha.1` - Alpha release
- `1.0.0-beta.1` - Beta release
- `1.0.0-rc.1` - Release candidate

## API Versioning

### URL Versioning
- Primary: `/api/v1/`
- Future: `/api/v2/`

### Header Versioning
- `Accept: application/vnd.quantx.v1+json`

### Deprecation Policy
- 6 months notice before removing endpoints
- Documentation maintained
- Migration guide provided

## Database Versioning

### Migration Files
```
infrastructure/database/migrations/
├── V1.0.0__initial_schema.sql
├── V1.1.0__add_positions_table.sql
└── V1.2.0__add_exchanges_indexes.sql
```

### Migration Strategy
- Alembic for PostgreSQL
- Native TimescaleDB partitioning
- Backward compatible migrations
- Roll-forward only

## Related Documents
- [50_RELEASE_PROCESS.md](50_RELEASE_PROCESS.md)
- [11_API_SPECIFICATION.md](11_API_SPECIFICATION.md)
- [08_DATABASE_DESIGN.md](08_DATABASE_DESIGN.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Operations*