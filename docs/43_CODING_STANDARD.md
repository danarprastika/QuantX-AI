---
status: Approved
owner: Engineering Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/43_CODING_STANDARD.md
depends_on:
  - docs/44_FOLDER_STRUCTURE.md
  - docs/45_PROJECT_CONVENTIONS.md
  - docs/34_TESTING.md
  - docs/15_SECURITY.md
related_documents:
  - docs/44_FOLDER_STRUCTURE.md
  - docs/45_PROJECT_CONVENTIONS.md
  - docs/34_TESTING.md
  - docs/15_SECURITY.md
---
# QuantX AI - Coding Standard

## Overview

This document defines the mandatory coding standards for all Python code in QuantX AI. Compliance is enforced through CI/CD pipelines with automated linting and formatting tools.

## Python Version Requirements

- **Minimum**: Python 3.11 (for structural pattern matching, improved type hints)
- **Target**: Python 3.11
- **Maximum**: Python 3.12 (until validated)

## Code Style

### Indentation and Formatting
- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Maximum 100 characters
- **Encoding**: UTF-8
- **End of Line**: LF (Unix style)

### String Formatting
- Use f-strings for string interpolation
- Triple-quoted strings for multi-line strings
- Raw strings (r"") for regex patterns

```python
# Good
name = f"Strategy {strategy.id}"
pattern = r"^[A-Z]{3,5}$"

# Bad
name = "Strategy " + str(strategy.id)
pattern = "^[A-Z]{3,5}$"  # Missing raw string
```

### Collections
- Use list/dict/set literals for empty collections
- Use `list()`, `dict()`, `set()` when initial size is known
- Prefer `defaultdict` over `setdefault` for aggregation

```python
# Good
items: list[str] = []
config: dict[str, Any] = {"key": "value"}

# Bad
items = list()  # Unnecessary for empty
```

## Type System

### Type Hints
All functions must include complete type hints:

```python
from typing import Optional, Union, List, Dict, Any
from services.trading.domain.entities import Strategy

def process_order(
    order_id: str,
    strategy: Optional[Strategy] = None,
) -> Union[ExecutionResult, OrderError]:
    ...
```

### Generic Aliases
Use `list[T]`, `dict[K, V]` syntax (Python 3.9+):

```python
# Good
def get_strategies() -> list[Strategy]:
    ...

# Avoid (legacy)
def get_strategies() -> List[Strategy]:
    ...
```

### Protocol Definitions
Use `Protocol` for structural subtyping:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class CacheProtocol(Protocol):
    def get(self, key: str) -> Optional[Any]: ...
    def set(self, key: str, value: Any) -> None: ...
```

### NewType for Semantic Types
```python
from typing import NewType

StrategyId = NewType('StrategyId', int)
Symbol = NewType('Symbol', str)

def get_strategy(id: StrategyId) -> Strategy:
    ...
```

## Documentation

### Docstring Format
Use Google-style docstrings with Types section:

```python
def execute_order(
    order: Order,
    exchange: ExchangeClient,
) -> ExecutionResult:
    """
    Execute an order on the specified exchange.
    
    Args:
        order: The order to execute
        exchange: Exchange client instance
        
    Returns:
        ExecutionResult containing details of the executed order
        
    Raises:
        ExchangeError: If exchange rejects the order
        InsufficientFundsError: If account lacks balance
    """
```

### Inline Comments
- Explain why, not what
- Update comments when code changes
- Remove outdated comments

```python
# Good
# Using 10-period SMA as per strategy requirements
sma = calculate_sma(prices, 10)

# Bad
# Calculate SMA
sma = calculate_sma(prices, 10)
```

## Error Handling

### Exception Classes
All custom exceptions inherit from `QuantXError`:

```python
class QuantXError(Exception):
    """Base exception for all QuantX errors."""
    pass

class ValidationError(QuantXError):
    """Input validation failure."""
    def __init__(self, message: str, field: str) -> None:
        self.message = message
        self.field = field
        super().__init__(f"{field}: {message}")
```

### Exception Handling
- Catch specific exceptions, not bare `except:`
- Never catch `Exception` or `BaseException`
- Use `raise from` for exception chaining

```python
# Good
try:
    result = api_call()
except requests.Timeout as e:
    raise APITimeoutError("API timeout") from e

# Bad
try:
    result = api_call()
except:
    pass
```

## Testing Standards

### Test Organization
- One test class per file
- Test class named after the class being tested
- Methods named `test_[method]_[condition]_[expected_result]`

```python
class TestStrategyService:
    def test_create_strategy_with_valid_config_creates_strategy(self): ...
    def test_create_strategy_with_invalid_config_raises_error(self): ...
```

### Assertions
Use pytest assertions with descriptive messages:

```python
assert strategy.status == StrategyStatus.ACTIVE, \
    f"Expected ACTIVE, got {strategy.status}"
```

### Fixtures
```python
@pytest.fixture
def strategy_repository() -> InMemoryStrategyRepository:
    return InMemoryStrategyRepository()

@pytest.fixture
def active_strategy() -> Strategy:
    return Strategy.create(
        name="Test Strategy",
        config=StrategyConfig(...)
    )
```

## Async/Await Conventions

### Async Functions
- Use `asyncio` for all I/O operations
- Always use `async` with `await`
- Never use `asyncio.get_event_loop()`

```python
# Good
async def fetch_market_data(symbol: Symbol) -> MarketData:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return MarketData(**response.json())

# Bad
def fetch_market_data(symbol: Symbol) -> MarketData:  # Not async
    ...
```

### Async Context Managers
```python
async with database.connection() as conn:
    result = await conn.fetch(query)
```

## Performance Standards

### Database Queries
- Never use `SELECT *`
- Always use parameterized queries
- Limit results when appropriate
- Include only needed columns

```python
# Good
SELECT id, symbol, quantity FROM positions WHERE user_id = $1 LIMIT 100

# Bad
SELECT * FROM positions WHERE user_id = ?
```

### Memory Management
- Use generators for large datasets
- Avoid accumulating objects in memory
- Process streams in chunks

```python
# Good - generator
def get_positions(user_id: int) -> Iterator[Position]:
    for row in db.fetch_iter(query, user_id):
        yield Position(**row)

# Bad - loads all into memory
def get_positions(user_id: int) -> list[Position]:
    return [Position(**row) for row in db.fetch_all(query, user_id)]
```

## Security Standards

### Input Validation
Always validate external input:

```python
def validate_symbol(symbol: str) -> Symbol:
    if not re.match(r'^[A-Z]{3,10}$', symbol):
        raise ValidationError("Invalid symbol format", "symbol")
    return Symbol(symbol)
```

### Secrets
Never log or expose secrets:

```python
# Good
logger.info("API key configured")  # No value logged

# Bad
logger.info(f"API key: {api_key}")  # Secret exposure
```

### SQL Injection Prevention
Always use parameterized queries:

```python
# Good
await db.execute(
    "SELECT * FROM positions WHERE user_id = $1",
    user_id
)

# Bad
await db.execute(
    f"SELECT * FROM positions WHERE user_id = {user_id}"  # SQL injection risk
)
```

## Linting and Formatting Tools

### ruff Configuration
```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = [
    "E", "F", "I", "N", "UP", "B", "C4", "SIM", "ARG"
]
ignore = ["ARG001"]  # Unused function arguments allowlist
```

### mypy Configuration
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_redundant_casts = true
warn_unused_ignores = true
```

### black Configuration
```toml
[tool.black]
line-length = 100
target-version = ["py311"]
```

## CI/CD Validation

### Pre-commit Hooks
- ruff check
- mypy check
- black format check
- trailing whitespace removal
- end-of-file fixer

### Pipeline Validation
- All checks must pass before merge
- Code coverage minimum 80%
- Type check strict mode
- Security scan with bandit

## Code Review Checklist

- [ ] All new code has type hints
- [ ] Functions have docstrings
- [ ] Tests cover new functionality
- [ ] No security issues identified
- [ ] Follows naming conventions
- [ ] Handles errors appropriately
- [ ] Performance considerations addressed
- [ ] No dead code or TODO comments

## Related Documents
- [44_FOLDER_STRUCTURE.md](44_FOLDER_STRUCTURE.md)
- [45_PROJECT_CONVENTIONS.md](45_PROJECT_CONVENTIONS.md)
- [34_TESTING.md](34_TESTING.md)
- [15_SECURITY.md](15_SECURITY.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Engineering Team*
*Source of Truth: docs/43_CODING_STANDARD.md*
*Depends On: 44_FOLDER_STRUCTURE.md, 45_PROJECT_CONVENTIONS.md, 34_TESTING.md, 15_SECURITY.md*
*Related Documents: 44_FOLDER_STRUCTURE.md, 45_PROJECT_CONVENTIONS.md, 34_TESTING.md, 15_SECURITY.md*
*Phase: Foundation*
