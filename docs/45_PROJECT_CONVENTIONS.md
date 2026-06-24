---
status: Approved
owner: Engineering Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/45_PROJECT_CONVENTIONS.md
depends_on:
  - docs/01_PROJECT_OVERVIEW.md
related_documents:
  - docs/01_PROJECT_OVERVIEW.md
---
# QuantX AI - Project Conventions

## Overview

This document defines the coding, architectural, and operational conventions for the QuantX AI project. These conventions ensure consistency, maintainability, and collaboration across all engineering teams.

## General Principles

### Code Quality Standards
1. **SOLID Principles**: All code must adhere to SOLID principles
2. **Clean Code**: Follow Robert Martin's Clean Code guidelines
3. **DRY**: Don't Repeat Yourself - shared code in `shared/`
4. **KISS**: Keep It Simple, Stupid - avoid unnecessary abstraction
5. **YAGNI**: You Aren't Gonna Need It - no premature optimization
6. **Boy Scout Rule**: Leave code cleaner than you found it

### Architectural Principles
1. **Dependency Inversion**: Depend on abstractions, not concretions
2. **Explicit is Better Than Implicit**: Clear contracts and interfaces
3. **Fail Fast**: Validate early, error clearly
4. **Single Responsibility**: Each module has one reason to change
5. **Open/Closed**: Modules open for extension, closed for modification

## Naming Conventions

### Variables and Functions
- Use descriptive names with full words
- No abbreviations except universally accepted (id, db, api)
- Private members prefixed with underscore
- Constants in UPPER_SNAKE_CASE

```python
# Good
user_identifier = "123"
database_connection = get_connection()
def calculate_portfolio_value(portfolio_id: str) -> Decimal:

# Bad
uid = "123"
db_conn = get_conn()
def calc_pv(pid: str) -> float:
```

### Classes and Interfaces
- PascalCase for all classes
- Interfaces end with `Protocol` or `Interface` suffix
- Abstract base classes end with `Base` suffix

```python
class OrderService:
class ExchangeClientProtocol:
class BaseRepository(ABC):
```

### Modules and Packages
- snake_case for Python modules
- kebab-case for directories
- Plural for collection modules, singular for domain modules

```
services/trading/
services/strategies/
shared/utils/
```

### Database Objects
| Object | Convention | Example |
|--------|------------|---------|
| Tables | snake_case, plural | `trading_positions` |
| Columns | snake_case | `entry_price` |
| Indexes | `idx_{table}_{columns}` | `idx_positions_strategy_id` |
| Constraints | `{type}_{table}_{column}` | `pk_users_id` |

### API Endpoints
- RESTful resource naming
- Plural nouns for collections
- Hyphenated paths

```
GET    /api/v1/strategies
POST   /api/v1/strategies
GET    /api/v1/strategies/{id}
PUT    /api/v1/strategies/{id}
DELETE /api/v1/strategies/{id}
```

## Coding Standards

### Python Style Guide

#### Imports
```python
# Standard library (alphabetical)
import asyncio
import json
from datetime import datetime
from decimal import Decimal
from typing import Optional

# Third-party (alphabetical)
import pytest
from fastapi import Depends, FastAPI

# Local (absolute imports)
from services.trading.domain.entities.strategy import Strategy
from shared.kernel.base import Entity
```

#### Type Hints
- All function parameters and returns must have type hints
- Use `Optional[T]` instead of `T | None` for compatibility
- Use `TypedDict` for structured dictionaries
- Use `NewType` for semantic types

```python
from typing import NewType, Optional, TypedDict

StrategyId = NewType('StrategyId', str)

class StrategyConfig(TypedDict):
    symbol: str
    timeframe: str
    risk_limit: Decimal

def get_strategy(id: StrategyId) -> Optional[Strategy]:
    ...
```

#### Docstrings
```python
def calculate_pnl(entry_price: Decimal, exit_price: Decimal, quantity: Decimal) -> Decimal:
    """
    Calculate profit and loss for a closed position.
    
    Args:
        entry_price: Price at which position was opened
        exit_price: Price at which position was closed
        quantity: Number of units traded
        
    Returns:
        Decimal representing profit or loss in quote currency
        
    Raises:
        ValueError: If any price is negative
    """
    ...
```

### Error Handling

#### Exception Hierarchy
```python
class QuantXError(Exception): ...
class DomainError(QuantXError): ...
class InfrastructureError(QuantXError): ...
class ValidationError(QuantXError): ...
```

#### Error Messages
- Include context (entity, operation, value)
- No sensitive data in messages
- User-facing vs system-facing distinction

```python
raise InsufficientFundsError(
    f"Account {account_id} has insufficient balance: "
    f"available {available} < required {required}"
)
```

### Configuration

#### Environment Variables
- Prefix: `QUANTX_`
- Snake case: `QUANTX_DATABASE_URL`
- Required vs optional documented in `.env.example`

#### Configuration Schema
```python
from pydantic import BaseSettings, Field

class DatabaseConfig(BaseSettings):
    url: str = Field(..., env='QUANTX_DATABASE_URL')
    pool_size: int = Field(default=20, env='QUANTX_DB_POOL_SIZE')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
```

## Domain Conventions

### Entity Design
```python
from uuid import UUID
from datetime import datetime
from shared.kernel import Entity

class Strategy(Entity):
    id: StrategyId
    user_id: UserId
    name: str
    config: StrategyConfig
    created_at: datetime
    updated_at: datetime
    
    def update_config(self, new_config: StrategyConfig) -> None:
        self.validate_config(new_config)
        self.config = new_config
        self.updated_at = datetime.utcnow()
        
    def validate_config(self, config: StrategyConfig) -> None:
        if config.risk_limit <= 0:
            raise ValidationError("Risk limit must be positive")
```

### Value Objects
- Immutable
- Self-validating
- No identity

```python
@dataclass(frozen=True)
class Symbol:
    base: str
    quote: str
    
    def __post_init__(self) -> None:
        if not self.base or not self.quote:
            raise ValueError("Symbol parts cannot be empty")
```

### Domain Events
```python
from shared.events.base import DomainEvent

class StrategyCreated(DomainEvent):
    strategy_id: StrategyId
    user_id: UserId
    strategy_type: StrategyType
```

## Service Conventions

### Command Handlers
- Return `Result` type or raise specific exceptions
- No return for commands that only create side effects
- Transactional boundaries explicit

```python
class CreateStrategy(CommandHandler[CreateStrategyCommand, StrategyId]):
    def __call__(self, command: CreateStrategyCommand) -> StrategyId:
        strategy = Strategy.create(
            user_id=command.user_id,
            name=command.name,
            config=command.config,
        )
        self.repository.save(strategy)
        self.event_publisher.publish(StrategyCreated(strategy.id, ...))
        return strategy.id
```

### Query Handlers
- Return DTOs or raise exceptions
- No side effects
- Caching hints in comments

```python
class GetPortfolio(QueryHandler[GetPortfolioQuery, PortfolioDTO]):
    def __call__(self, query: GetPortfolioQuery) -> PortfolioDTO:
        ...
```

### Application Services
- Orchestrate domain operations
- Handle cross-cutting concerns
- Stateless

## Testing Conventions

### Test Naming
```
Given_When_Then naming convention
services/trading/tests/unit/test_strategy_creation.py
```

### Test Structure
```python
def test_given_valid_config_when_creating_strategy_then_strategy_is_created():
    # Given
    config = StrategyConfig(symbol="BTCUSDT", ...)
    
    # When
    strategy = Strategy.create(user_id=user_id, config=config)
    
    # Then
    assert strategy.id is not None
    assert strategy.status == StrategyStatus.DRAFT
```

### Fixture Naming
- `fixture_` prefix for clarity
- Descriptive names matching tested concepts

```python
@pytest.fixture
def fixture_active_strategy() -> Strategy:
    ...
```

## Git Conventions

### Branch Naming
```
type/scope: description

feature/trading/add-order-execution
fix/auth/resolve-token-refresh-bug
chore/deps/update-dependencies
```

### Commit Messages
```
type(scope): subject

feature(trading): add market order execution with slippage protection

- Implement order service with validation
- Add slippage calculation based on order book depth
- Update exchange adapter for Binance
```

## Documentation Conventions

### Document Headers
Each document starts with:
```markdown
# QuantX AI - [Document Name]

[Purpose statement]

...content...

## Related Documents
- [XX_DOCUMENT_NAME.md](XX_DOCUMENT_NAME.md)

---
*Document Version: 1.0.0*
*Created: YYYY-MM-DD*
*Phase: [Phase Name]*
```

### ADR Format
- Title, Status, Context, Decision, Consequences
- Link to related documents
- Date and author

## Operational Conventions

### Logging Format
```python
logger.info(
    "Order executed",
    extra={
        "order_id": order.id,
        "symbol": order.symbol,
        "side": order.side,
        "quantity": order.quantity,
        "price": order.price,
    }
)
```

### Metrics Naming
- `_total` for counters
- `_seconds` for histograms
- `_ratio` for gauges

```
quantx_orders_executed_total{exchange="binance", symbol="BTCUSDT"}
quantx_prediction_latency_seconds{strategy_type="lstm"}
quantx_active_connections_ratio{service="telegram"}
```

## Security Conventions

### Secrets Management
- Never in code or config files
- Use environment variables or Vault
- Rotate regularly
- Audit access

### Input Validation
- All external input validated
- Use Pydantic models
- Sanitization for Telegram messages
- Rate limiting on all endpoints

## Version Control Conventions

### Semantic Versioning
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

### Tagging
```
v1.0.0
v1.0.0-rc1
v1.0.0-beta.1
```

## Related Documents
- [43_CODING_STANDARD.md](43_CODING_STANDARD.md)
- [44_FOLDER_STRUCTURE.md](44_FOLDER_STRUCTURE.md)
- [41_GIT_WORKFLOW.md](41_GIT_WORKFLOW.md)
- [27_CONFIGURATION.md](27_CONFIGURATION.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Engineering Team*
*Source of Truth: docs/45_PROJECT_CONVENTIONS.md*
*Depends On: 01_PROJECT_OVERVIEW.md*
*Related Documents: 01_PROJECT_OVERVIEW.md*
*Phase: [Phase Name]*
