# QuantX AI

Algorithmic Trading Platform

## Goals

QuantX AI is a production-ready algorithmic trading platform designed to automate strategy execution, manage risk, and provide real-time analytics through a modern web interface and Telegram bot.

## Architecture Overview

The project follows Clean Architecture (Onion Architecture) with strict separation of concerns across multiple services:

- **Backend (FastAPI)** - High-performance async API layer
- **Frontend (React + Vite)** - Modern web dashboard
- **Telegram Bot (aiogram)** - Conversational trading interface
- **Worker (Celery)** - Background job processing
- **Shared Libraries** - Domain kernel and cross-cutting utilities

Each service follows the same architectural layers:
1. Domain (entities, value objects, repositories)
2. Application (use cases, commands, queries)
3. Infrastructure (database, cache, messaging)
4. Presentation (controllers, middleware, serializers)

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Runtime | Python 3.11+, Node.js 20 |
| Backend | FastAPI, Uvicorn, SQLAlchemy 2, Alembic |
| Frontend | React 18, TypeScript 5, Vite, Tailwind CSS |
| State | TanStack Query, Zustand |
| Bot | aiogram 3.x |
| Queue | Celery + Redis, RabbitMQ |
| Cache | Redis |
| Database | PostgreSQL 16, TimescaleDB |
| Observability | OpenTelemetry, Prometheus, Grafana |
| Quality | ruff, mypy, pytest |

## Repository Structure

```
backend/          # FastAPI application
bot/              # Telegram bot service
frontend/         # React web application
worker/           # Celery background workers
shared/           # Cross-service shared libraries
infrastructure/   # IaC placeholders
scripts/          # Operational scripts
api/              # OpenAPI and contract schemas
docs/             # Approved documentation
tests/            # Cross-service tests
services/         # Future service modules
```

## Quick Start

```bash
# Install Python dependencies
pip install -e backend -e bot -e worker -e shared/python

# Install frontend dependencies
cd frontend && npm install && cd ..

# Copy environment configuration
cp .env.example .env

# Start all services
docker-compose up -d
```

## Docker

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## Development Workflow

```bash
# Run linters
make lint

# Format code
make format

# Type check
make typecheck

# Run tests
make test
```

## Testing

- **Backend**: pytest with pytest-asyncio
- **Frontend**: ESLint + TypeScript compiler
- **Integration**: Docker Compose environments

## Documentation

See [docs/](docs/) for complete architecture and design documentation.

## CI/CD

GitHub Actions workflows automate linting, type checking, testing, and Docker build verification on every push and pull request.

## Roadmap

- Sprint 1: Project Foundation (complete)
- Sprint 2: Service Skeleton & Data Layer
- Sprint 3: Trading Core
- Sprint 4: AI Pipeline
- Sprint 5: Telegram Integration
- Sprint 6: Observability & Hardening

## License

MIT

## Contribution

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

All contributions must pass lint, type check, and test quality gates.
