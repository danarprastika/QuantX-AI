# QuantX Platform Architecture

This document describes the architecture of the QuantX Platform Backend.

## Architecture Layers (MDS Section 50)

```
Presentation → Application → Domain → Infrastructure
```

Dependencies point inward only. Outer layers may depend on inner layers through interfaces.

### Layer Responsibilities

| Layer | Depends On | Responsibility |
|-------|------------|----------------|
| Domain | None | Business logic, invariants |
| Application | Domain | Use cases, orchestration |
| Infrastructure | Application/Domain | External integrations |
| Presentation | Application | User interface, transport |

## Bounded Contexts

Per MDS Section 49, each bounded context contains:
- `entities/` - Domain entities
- `value-objects/` - Immutable value objects
- `repositories/` - Repository interfaces (Domain layer only, per MDS 49.7)
- `events/` - Domain events (per MDS 46)

## Technology Stack (MDS Section 36)

- **Backend:** NestJS LTS / TypeScript Stable
- **ORM:** Prisma ORM
- **Database:** PostgreSQL
- **Cache:** Redis
- **Queue:** BullMQ
- **Auth:** JWT / OAuth2 / RBAC