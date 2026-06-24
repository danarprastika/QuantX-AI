# QuantX AI - Folder Structure

## Repository Organization

```
quantx-ai/
├── .github/                    # GitHub workflows and templates
│   ├── workflows/             # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── PULL_REQUEST_TEMPLATE/ # PR templates
│
├── .kilo/                     # Kilo configuration
│   ├── agent/                 # Agent configurations
│   ├── command/               # Custom commands
│   └── plans/                 # Project plans
│
├── docs/                      # Documentation (this directory)
│   ├── ADR/                   # Architecture Decision Records (symlink)
│   └── diagrams/              # Architecture diagrams
│
├── infrastructure/            # Infrastructure as Code
│   ├── terraform/            # AWS/Azure provisioning
│   │   ├── modules/          # Reusable modules
│   │   ├── environments/     # env-specific configurations
│   │   └── providers/        # Cloud provider configs
│   ├── k8s/                # Kubernetes manifests
│   │   ├── charts/         # Helm charts
│   │   ├── base/           # Base configurations
│   │   └── overlays/       # Environment overlays
│   └── docker/             # Custom docker images
│
├── scripts/                  # Operational scripts
│   ├── deployment/         # Deployment automation
│   ├── migration/          # Database migrations
│   ├── backup/             # Backup scripts
│   └── setup/             # Environment setup
│
├── tests/                   # Integration and E2E tests
│   ├── integration/        # Service integration tests
│   ├── e2e/              # End-to-end tests
│   ├── conftest.py         # Shared test configuration
│   └── pytest.ini           # Test configuration
│
├── services/                # Application services
│   ├── __init__.py
│   │
│   ├── trading/            # Trading service
│   │   ├── __init__.py
│   │   ├── adapters/       # Exchange adapters
│   │   ├── commands/       # Command handlers
│   │   ├── queries/        # Query handlers
│   │   ├── domain/         # Trading domain logic
│   │   ├── application/    # Application services
│   │   └── infrastructure/ # External integrations
│   │
│   ├── strategy/           # Strategy management service
│   │   ├── __init__.py
│   │   ├── ai/             # AI model implementations
│   │   ├── backtest/       # Backtesting engine
│   │   ├── domain/         # Strategy domain logic
│   │   ├── application/    # Strategy application services
│   │   └── infrastructure/ # Strategy infrastructure
│   │
│   ├── market-data/          # Market data service
│   │   ├── __init__.py
│   │   ├── collectors/     # Data collectors
│   │   ├── processors/     # Data processors
│   │   ├── domain/         # Market data domain
│   │   ├── application/    # Application layer
│   │   └── infrastructure/ # Infrastructure integrations
│   │
│   ├── user-auth/            # User authentication service
│   │   ├── __init__.py
│   │   ├── auth/           # Authentication logic
│   │   ├── domain/         # User domain
│   │   ├── application/    # Application services
│   │   └── infrastructure/ # External integrations
│   │
│   ├── telegram/             # Telegram bot service
│   │   ├── __init__.py
│   │   ├── handlers/       # Bot handlers
│   │   ├── domain/         # Telegram domain
│   │   ├── application/    # Application logic
│   │   └── infrastructure/ # Bot infrastructure
│   │
│   ├── portfolio/            # Portfolio tracking service
│   │   ├── __init__.py
│   │   ├── analytics/      # Analytics engine
│   │   ├── domain/         # Portfolio domain
│   │   ├── application/    # Application layer
│   │   └── infrastructure/ # External integrations
│   │
│   └── notification/         # Notification service
│       ├── __init__.py
│       ├── providers/      # Notification providers
│       ├── domain/         # Notification domain
│       ├── application/    # Application layer
│       └── infrastructure/ # Infrastructure layer
│
├── shared/                  # Shared components
│   ├── __init__.py
│   ├── kernel.py           # Core domain kernel
│   ├── events/             # Event definitions
│   ├── errors/             # Shared error types
│   ├── config/             # Configuration schemas
│   ├── utils/              # Utility functions
│   ├── types/              # Shared type definitions
│   └── constants/          # Shared constants
│
├── api/                     # API definitions
│   ├── openapi.yaml          # OpenAPI 3.0 specification
│   ├── contracts/            # API contracts (protobuf)
│   └── schemas/              # JSON schemas
│
├── src/                     # Main application source (legacy structure)
│   ├── quantx/              # Main package
│   │   ├── __init__.py
│   │   ├── main.py          # Application entry point
│   │   └── config.py        # Application configuration
│   └── manage.py            # Management script
│
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── docker-compose.yml       # Local development environment
├── docker-compose.prod.yml  # Production override
├── pyproject.toml           # Python project configuration
├── Makefile               # Development shortcuts
└── README.md                # Project README
```

## Service Layer Structure

Each service follows Clean Architecture principles with four concentric layers:

```
services/{service-name}/
├── __init__.py
│
├── adapters/               # INTERFACE ADAPTERS (Outer)
│   ├── inbound/           # Inbound adapters (controllers, handlers)
│   │   └── telegram_handler.py
│   └── outbound/          # Outbound adapters (repositories, gateways)
│       ├── repository.py
│       └── exchange_client.py
│
├── domain/                # DOMAIN LAYER (Inner)
│   ├── __init__.py
│   ├── entities/          # Business entities
│   │   └── strategy.py
│   ├── value_objects/     # Value objects
│   │   └── symbol.py
│   ├── services/          # Domain services
│   └── repositories/      # Repository interfaces
│       └── strategy_repository.py
│
├── application/           # APPLICATION LAYER
│   ├── __init__.py
│   ├── commands/          # Command handlers
│   │   └── create_strategy.py
│   ├── queries/           # Query handlers
│   │   └── get_portfolio.py
│   ├── services/          # Application services
│   └── dtos/              # Data transfer objects
│
├── infrastructure/        # INFRASTRUCTURE LAYER
│   ├── __init__.py
│   ├── config.py          # Service configuration
│   ├── container.py       # DI container
│   └── logger.py          # Service-specific logging
│
└── tests/                # Service tests
    ├── unit/             # Unit tests
    ├── integration/      # Integration tests
    └── conftest.py       # Test fixtures
```

## Infrastructure Structure

```
infrastructure/
├── terraform/
│   ├── modules/
│   │   ├── database/     # Database module
│   │   ├── compute/      # Compute resources
│   │   ├── networking/   # VPC, subnets, etc.
│   │   ├── security/     # IAM, security groups
│   │   └── monitoring/   # Monitoring resources
│   │
│   ├── environments/
│   │   ├── prod/         # Production
│   │   ├── staging/      # Staging
│   │   └── dev/          # Development
│   │
│   └── providers/
│       ├── aws/          # AWS provider
│       └── azure/        # Azure provider (backup)
│
├── k8s/
│   ├── charts/
│   │   ├── trading/      # Trading service chart
│   │   ├── strategy/     # Strategy service chart
│   │   ├── market-data/  # Market data chart
│   │   ├── user-auth/    # Auth service chart
│   │   ├── telegram/     # Telegram chart
│   │   ├── portfolio/    # Portfolio chart
│   │   └── notification/ # Notification chart
│   │
│   ├── base/
│   │   ├── namespaces/   # Kubernetes namespaces
│   │   ├── secrets/      # Secret templates
│   │   └── rbac/         # RBAC definitions
│   │
│   └── overlays/
│       ├── prod/         # Production overlay
│       ├── staging/      # Staging overlay
│       └── dev/          # Development overlay
```

## Shared Components Structure

```
shared/
├── kernel.py              # Enterprise kernel with base classes
│
├── events/
│   ├── __init__.py
│   ├── base.py            # Base event class
│   ├── domain_events.py   # Domain events
│   └── integration_events.py # Integration events
│
├── errors/
│   ├── __init__.py
│   ├── base.py            # Base error class
│   ├── domain_errors.py   # Domain-specific errors
│   └── infrastructure_errors.py # Infrastructure errors
│
├── config/
│   ├── __init__.py
│   ├── settings.py        # Pydantic settings
│   └── feature_flags.py   # Feature flag definitions
│
├── utils/
│   ├── __init__.py
│   ├── crypto.py          # Cryptographic utilities
│   ├── datetime.py        # DateTime utilities
│   └── validation.py      # Validation utilities
│
├── types/
│   ├── __init__.py
│   ├── money.py           # Money/Value types
│   ├── symbol.py          # Trading symbol type
│   └── side.py          # Buy/Sell side enum
│
└── constants/
    ├── __init__.py
    ├── exchanges.py       # Exchange constants
    ├── symbols.py         # Trading symbol defaults
    └── risk_limits.py     # Risk management limits
```

## API Layer Structure

```
api/
├── openapi.yaml           # Canonical API spec
│
├── contracts/
│   ├── v1/              # API version 1
│   │   ├── trading.proto
│   │   ├── strategy.proto
│   │   ├── market.proto
│   │   └── user.proto
│   │
│   └── v2/              # Future versions
│
└── schemas/
    ├── requests/          # Request schemas
    │   ├── strategy_create.json
    │   └── order_place.json
    │
    └── responses/         # Response schemas
        ├── prediction.json
        └── portfolio.json
```

## Testing Structure

```
tests/
├── conftest.py            # Root pytest configuration
│
├── unit/
│   ├── services/          # Service unit tests
│   ├── domain/            # Domain unit tests
│   └── shared/            # Shared utility tests
│
├── integration/
│   ├── api/               # API integration tests
│   ├── database/          # Database integration tests
│   └── external/          # External service tests
│
├── e2e/
│   ├── trading_flow/      # Trading workflow tests
│   ├── strategy_flow/     # Strategy workflow tests
│   └── telegram_flow/     # Telegram workflow tests
│
└── fixtures/
    ├── factories/         # Test data factories
    ├── mocks/             # Mock implementations
    └── seed_data/         # Seed data for tests
```

## Scripts Structure

```
scripts/
├── deployment/
│   ├── deploy.sh          # Deployment script
│   ├── rollback.sh        # Rollback script
│   └── health_check.sh    # Health check script
│
├── migration/
│   ├── migrate.py         # Migration runner
│   └── versions/          # Migration scripts
│
├── backup/
│   ├── backup.sh          # Backup script
│   ├── restore.sh         # Restore script
│   └── verify.sh          # Backup verification
│
└── setup/
    ├── local.sh           # Local environment setup
    ├── dev.sh             # Dev environment setup
    └── prod.sh            # Production setup helper
```

## Directory Naming Conventions

| Pattern | Description | Example |
|---------|-------------|---------|
| kebab-case | All directories | `market-data` |
| snake_case | Python modules | `market_data` |
| PascalCase | Classes | `StrategyService` |

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Python modules | snake_case | `strategy_service.py` |
| Config files | kebab-case | `docker-compose.prod.yml` |
| Documentation | UPPER_SNAKE_CASE | `01_PROJECT_OVERVIEW.md` |
| Scripts | kebab-case | `deploy-service.sh` |

## Import Organization

```python
# Standard library imports
import asyncio
import logging
from datetime import datetime

# Third-party imports
import pytest
from fastapi import FastAPI

# Local imports (absolute)
from services.trading.domain.entities import Strategy
from shared.kernel import Entity
from api.schemas.requests import StrategyCreate
```

## Related Documents
- [43_CODING_STANDARD.md](43_CODING_STANDARD.md)
- [45_PROJECT_CONVENTIONS.md](45_PROJECT_CONVENTIONS.md)
- [06_CLEAN_ARCHITECTURE.md](06_CLEAN_ARCHITECTURE.md)
- [22_BACKEND_ARCHITECTURE.md](22_BACKEND_ARCHITECTURE.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Foundation*