---
status: Approved
owner: Backend Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/28_DEPENDENCY_INJECTION.md
depends_on:
  - docs/27_CONFIGURATION.md
  - docs/06_CLEAN_ARCHITECTURE.md
  - docs/44_FOLDER_STRUCTURE.md
related_documents:
  - docs/27_CONFIGURATION.md
  - docs/06_CLEAN_ARCHITECTURE.md
  - docs/44_FOLDER_STRUCTURE.md
---
# QuantX AI - Dependency Injection

## Overview

This document defines the dependency injection architecture for QuantX AI, including container patterns, service registration, lifecycle management, and testing strategies.

## DI Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Dependency Injection Layers                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │   Services   │  │   Adapters   │  │   Clients    │  │   Repos      │ │
│   │              │  │              │  │              │  │              │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼─────────────────────────────────────────────────────────────┐    │
│   │                    DI Container                                     │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐                        │    │
│   │  │ Service  │  │ Factory  │  │ Singleton│                        │    │
│   │  │ Providers│  │ Providers│  │ Providers│                        │    │
│   │  └──────────┘  └──────────┘  └──────────┘                        │    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Trading    │  │   Strategy   │  │   Market     │  │   User       │ │
│  │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Container Pattern

### Service Container
```python
class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # Gateways
    database = providers.Singleton(DatabaseManager)
    message_queue = providers.Singleton(MessageQueueConnection)
    cache = providers.Singleton(RedisClient)
    
    # Repositories
    strategy_repo = providers.Singleton(
        PostgresStrategyRepository,
        pool=database.provided.pool
    )
    position_repo = providers.Singleton(
        PostgresPositionRepository,
        pool=database.provided.pool
    )
    
    # Services
    exchange_client = providers.Singleton(
        BinanceExchangeAdapter,
        api_key=config.exchange.binance_api_key,
        api_secret=config.exchange.binance_api_secret,
    )
    
    # Use Cases
    create_strategy = providers.Singleton(
        CreateStrategy,
        strategy_repo=strategy_repo,
        event_publisher=message_queue.provided.event_publisher,
    )
```

### Component Registration
```python
# Infrastructure registration
container.database_pool.from_env("QUANTX_DATABASE_POOL_SIZE", default=20)
container.redis_url.from_env("QUANTX_REDIS_URL")
container.exchange_api_key.from_env("QUANTX_EXCHANGE_API_KEY")

# Protocol-based registration
container.register(
    StrategyRepository, 
    PostgresStrategyRepository
)
container.register(
    ExchangeClient, 
    BinanceExchangeAdapter
)
```

## Provider Types

### Singleton
- One instance per container
- Cached after first resolution
- Used for: Repositories, Clients, Services

```python
db_pool = providers.Singleton(create_connection_pool)
```

### Factory
- New instance each resolution
- Used for: HTTP requests, Commands, Queries

```python
strategy_validator = providers.Factory(StrategyValidator)
```

### Delegated
- Delegates to parent container
- Used for: Shared configuration

```python
shared_config = providers.Delegated(Configuration)
```

## Lifecycle Management

### Startup
```python
async def initialize_container() -> Container:
    """Initialize DI container with connections."""
    container.config.from_yaml("config.yaml")
    container.config.from_env(".env")
    
    # Initialize connections
    await container.database.connect()
    await container.message_queue.connect()
    await container.cache.connect()
    
    return container
```

### Shutdown
```python
async def shutdown_container(container: Container) -> None:
    """Clean shutdown of all dependencies."""
    await container.message_queue.disconnect()
    await container.database.disconnect()
    await container.cache.disconnect()
```

## Wire Structure

### Service Wiring
```python
# services/trading/__init__.py
from dependency_injector import containers
from dependency_injector.wiring import inject, Provide

@inject
async def open_position(
    command: OpenPositionCommand,
    position_repo: PositionRepository = Provide[Container.position_repo],
    exchange_client: ExchangeClient = Provide[Container.exchange_client],
) -> PositionId:
    ...
```

### Async Support
```python
class AsyncContainer(containers.DeclarativeContainer):
    async def resolve_async(self, protocol: Type[T]) -> T:
        instance = self._services.get(protocol)
        if hasattr(instance, 'initialize'):
            await instance.initialize()
        return instance
```

## Testing with DI

### Mock Providers
```python
# Test container
class TestContainer(TradingContainer):
    def __init__(self) -> None:
        super().__init__()
        self.strategy_repo.override(providers.Singleton(MockStrategyRepository))
        self.exchange_client.override(providers.Singleton(MockExchangeClient))
```

### Fixture Integration
```python
@pytest.fixture
def di_container() -> Container:
    container = TestContainer()
    container.config.from_value({
        "database": {"url": "sqlite:///:memory:"},
        "exchange": {"testnet": True},
    })
    return container
```

## Related Documents
- [27_CONFIGURATION.md](27_CONFIGURATION.md)
- [06_CLEAN_ARCHITECTURE.md](06_CLEAN_ARCHITECTURE.md)
- [44_FOLDER_STRUCTURE.md](44_FOLDER_STRUCTURE.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Backend Team*
*Source of Truth: docs/28_DEPENDENCY_INJECTION.md*
*Depends On: 27_CONFIGURATION.md, 06_CLEAN_ARCHITECTURE.md, 44_FOLDER_STRUCTURE.md*
*Related Documents: 27_CONFIGURATION.md, 06_CLEAN_ARCHITECTURE.md, 44_FOLDER_STRUCTURE.md*
*Phase: Infrastructure*
