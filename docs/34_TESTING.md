# QuantX AI - Testing

## Overview

This document defines the testing strategy for QuantX AI, including test types, frameworks, coverage requirements, fixtures, and quality gates.

## Testing Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Testing Layers                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │  Unit Tests  │  │ Integration  │  │    E2E       │  │ Performance  │ │
│   │              │  │   Tests      │  │   Tests      │  │   Tests      │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼─────────────────────────────────────────────────────────────┐    │
│   │                    Test Runner (pytest)                             │    │
│   │  Discovers, runs, reports on all tests                             │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Coverage     │  │   Report     │  │   Quality    │  │   Gate       │ │
│  │   Tool       │  │   Generator  │  │   Checker    │  │   Enforcer   │ │
│   │  (Coverage)  │  │  (Allure)    │  │  (SonarQube) │  │  (CI/CD)     │ │
│   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Test Types and Coverage

### Unit Tests (70% of test suite)
- Domain entity tests
- Use case tests
- Utility function tests
- Mock external dependencies
- Coverage target: 85% minimum

### Integration Tests (20% of test suite)
- API endpoint tests
- Database integration
- Message queue integration
- Cache integration
- Coverage target: 75% of service coverage

### End-to-End Tests (10% of test suite)
- User journey tests
- Cross-service flows
- Production-like environment
- Coverage target: Critical paths

## Testing Frameworks

### Python Testing Stack
| Purpose | Tool | Configuration |
|---------|------|---------------|
| Test runner | pytest | pytest.ini |
| Mocking | pytest-mock | unittest.mock |
| Property testing | hypothesis | strict mode |
| Load testing | locust | loadtest/locust |
| Coverage | coverage.py | branch coverage |
| Code quality | ruff, mypy | pyproject.toml |

### Frontend Testing Stack
| Purpose | Tool |
|---------|------|
| Component testing | React Testing Library |
| E2E testing | Playwright |
| Linting | ESLint, Prettier |

## Test Organization

### Directory Structure
```
tests/
├── unit/                    # Unit tests
│   ├── services/           # Service unit tests
│   ├── domain/             # Domain tests
│   └── shared/             # Shared code tests
├── integration/            # Integration tests
│   ├── api/               # API tests
│   ├── database/          # Database tests
│   └── external/          # External service tests
├── e2e/                   # End-to-end tests
├── fixtures/             # Test fixtures
├── conftest.py           # Shared config
└── pytest.ini            # Configuration
```

## Test Fixtures

### Repository Fixtures
```python
@pytest.fixture
def strategy_repository() -> InMemoryStrategyRepository:
    return InMemoryStrategyRepository()

@pytest.fixture
def exchange_client() -> MockExchangeClient:
    return MockExchangeClient()

@pytest.fixture
def user_service(
    strategy_repository: StrategyRepository,
    exchange_client: ExchangeClient,
) -> UserService:
    return UserService(
        strategy_repo=strategy_repository,
        exchange_client=exchange_client,
    )
```

### Factory Fixtures
```python
@pytest.fixture
def factory() -> Factory:
    return Factory()

def strategy(
    factory: Factory,
    user_id: UserId = None,
) -> Strategy:
    return factory.strategy.create(user_id=user_id)
```

## Quality Gates

### CI/CD Test Requirements
| Metric | Threshold | Failure Action |
|--------|-----------|----------------|
| Unit Test Pass Rate | 100% | Block merge |
| Integration Test Pass Rate | 100% | Block merge |
| E2E Test Pass Rate | 95% | Block production deploy |
| Coverage | 80% | Block merge |
| Security Issues | 0 critical | Block merge |
| Linting Errors | 0 | Block merge |

### Performance Test Requirements
- Response time < 100ms for 95th percentile
- Error rate < 1% under load
- No memory leaks over 1 hour
- CPU usage < 80% at peak

## Related Documents
- [43_CODING_STANDARD.md](43_CODING_STANDARD.md)
- [40_CI_CD.md](40_CI_CD.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Operations*