# Application Layer

## Responsibility

The application layer orchestrates the flow of data between the domain layer and the outside world.
It contains use cases, application services, commands, queries, and data transfer objects (DTOs).

## Contents

- **use_cases/** - Application-specific business rules
- **services/** - Application services that coordinate domain objects
- **dtos/** - Data transfer objects for input/output
- **ports/** - Interfaces (ports) for external dependencies

## Rules

- Depends only on the domain layer
- Knows nothing about the presentation, infrastructure, or frameworks
- Coordinates domain objects to fulfill application-specific tasks
