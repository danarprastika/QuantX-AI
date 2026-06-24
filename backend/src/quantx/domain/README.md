# Domain Layer

## Responsibility

The domain layer contains the core business logic and rules of the application.
It is the heart of the system and must remain independent of all other layers.

## Contents

- **entities/** - Business entities with identity and behavior
- **value_objects/** - Immutable value objects
- **services/** - Domain services for complex business logic
- **repositories/** - Repository interfaces (protocols)
- **events/** - Domain events

## Rules

- Zero external dependencies (no framework imports)
- Pure Python, focused on business rules
- Entities contain behavior, not just data
- Repository interfaces are defined here, implemented elsewhere
