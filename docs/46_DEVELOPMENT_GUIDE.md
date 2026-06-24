---
status: Approved
owner: Engineering Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/46_DEVELOPMENT_GUIDE.md
depends_on:
  - docs/43_CODING_STANDARD.md
  - docs/44_FOLDER_STRUCTURE.md
  - docs/45_PROJECT_CONVENTIONS.md
  - docs/01_PROJECT_OVERVIEW.md
related_documents:
  - docs/43_CODING_STANDARD.md
  - docs/44_FOLDER_STRUCTURE.md
  - docs/45_PROJECT_CONVENTIONS.md
  - docs/01_PROJECT_OVERVIEW.md
---
# QuantX AI - Development Guide

## Overview

This document provides the development guide for contributing to QuantX AI, including setup instructions, development workflow, testing procedures, and contribution guidelines.

## Prerequisites

### Required Tools
- Python 3.11+
- Poetry 1.8+
- Docker 25+
- Docker Compose 2.20+
- kubectl 1.29+
- Helm 3.14+

### Optional Tools
- VS Code with extensions
- Postman/Bruno for API testing
- Telegram bot testing account

## Development Setup

### Local Environment
```bash
# Clone repository
git clone https://github.com/quantx-ai/quantx-ai.git
cd quantx-ai

# Install dependencies
poetry install

# Setup environment
cp .env.example .env
# Edit .env with your values

# Start infrastructure
docker-compose up -d

# Run migrations
poetry run alembic upgrade head

# Start development server
poetry run uvicorn src.quantx.main:app --reload
```

## Project Structure
```
quantx-ai/
├── services/           # Service implementations
├── shared/             # Shared utilities
├── infrastructure/     # IaC definitions
├── tests/              # Test suites
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/my-feature develop
```

### 2. Develop and Test
```bash
# Run tests
poetry run pytest

# Run linting
poetry run ruff check .
poetry run mypy .
```

### 3. Commit Changes
```bash
git add .
git commit -m "feature(trading): add order validation"
```

## Testing During Development
```bash
# Run specific tests
poetry run pytest tests/unit/test_trading.py -v

# Run with coverage
poetry run pytest --cov=services.trading

# Run lint and type check
poetry run ruff check . && poetry run mypy .
```

## Code Standards
- Follow PEP 8 and project conventions
- Type hints required
- Docstrings required for public functions
- Tests required for business logic

## Related Documents
- [43_CODING_STANDARD.md](43_CODING_STANDARD.md)
- [44_FOLDER_STRUCTURE.md](44_FOLDER_STRUCTURE.md)
- [45_PROJECT_CONVENTIONS.md](45_PROJECT_CONVENTIONS.md)
- [01_PROJECT_OVERVIEW.md](01_PROJECT_OVERVIEW.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Engineering Team*
*Source of Truth: docs/46_DEVELOPMENT_GUIDE.md*
*Depends On: 43_CODING_STANDARD.md, 44_FOLDER_STRUCTURE.md, 45_PROJECT_CONVENTIONS.md, 01_PROJECT_OVERVIEW.md*
*Related Documents: 43_CODING_STANDARD.md, 44_FOLDER_STRUCTURE.md, 45_PROJECT_CONVENTIONS.md, 01_PROJECT_OVERVIEW.md*
*Phase: Operations*
