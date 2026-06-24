# Presentation Layer

## Responsibility

The presentation layer handles all interaction with the outside world.
It translates external input into commands for the application layer and formats responses for the caller.

## Contents

- **controllers/** - HTTP controllers (FastAPI routers)
- **middleware/** - Request/response middleware
- **serializers/** - Request/response serialization (Pydantic schemas)
- **errors/** - HTTP exception handlers and error responses

## Rules

- Depends only on the application and domain layers
- No business logic
- Responsible only for input validation and output formatting
- Translates between external formats and internal DTOs
