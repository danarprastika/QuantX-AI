# Infrastructure Layer

## Responsibility

The infrastructure layer provides implementations for interfaces defined in the domain and application layers.
It handles external concerns such as databases, caches, message queues, and third-party APIs.

## Contents

- **repositories/** - Implementations of repository interfaces
- **services/** - External service clients (exchanges, AI models, etc.)
- **messaging/** - Message queue and event bus implementations
- **persistence/** - Database and ORM configurations
- **external_apis/** - Clients for external systems

## Rules

- Implements interfaces defined by inner layers
- Contains framework-specific code
- Handles I/O operations, network calls, and data serialization
- Must be replaceable without affecting business logic
