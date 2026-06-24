# Shared Kernel

## Responsibility

The shared kernel contains code that is used across multiple layers and services.
It must remain stable and free of business logic.

## Contents

- **events/** - Shared event definitions
- **errors/** - Shared exception types
- **types/** - Shared type definitions
- **constants/** - Shared constants
- **utils/** - General utility functions

## Rules

- No business logic
- Must be importable by any layer
- Changes here affect the entire system; proceed with caution
- Keep it small and focused
