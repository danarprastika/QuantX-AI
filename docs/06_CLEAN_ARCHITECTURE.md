# QuantX AI - Clean Architecture

## Overview

QuantX AI implements Clean Architecture (Onion Architecture) to achieve loose coupling, testability, and framework independence. This document describes the architecture principles, layer responsibilities, and dependency rules.

## Architecture Principles

### Dependency Rule
Source code dependencies must point inward. Inner layers define interfaces; outer layers implement them.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRAMEWORK/INTERFACE                           │
│                         (Web, DB, External APIs)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                             ADAPTERS                                  │
│                      (Controllers, Presenters, Gateways)                  │
├─────────────────────────────────────────────────────────────────────────┤
│                         USE CASES INTERACTOR                            │
│                   (Application Business Rules)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                              ENTITIES                                   │
│                    (Enterprise Business Rules)                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Principles Applied

1. **Framework Independence**: Core business logic free from frameworks
2. **Testability**: Business rules testable without UI, database, or web server
3. **UI Independence**: UI can change without affecting business rules
4. **Database Independence**: Business logic doesn't know about database
5. **External Agency Independence**: Business logic unaware of external systems

## Layer Definitions

### Layer 1: Entities (Domain Layer)

**Location**: `services/{service}/domain/entities/`

**Responsibility**: 
- Enterprise-wide business rules
- Domain model definition
- Entity invariants and behavior

**Characteristics**:
- Pure Python, no external dependencies
- No knowledge of application, infrastructure, or UI
- Entities contain business logic, not just data

```python
# Example entity (pure domain, no imports from outer layers)
class Strategy:
    def __init__(
        self,
        id: StrategyId,
        user_id: UserId,
        name: StrategyName,
        config: StrategyConfig,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.name = name
        self.config = config
    
    def activate(self) -> None:
        if not self.config.is_valid():
            raise InvalidStrategyError("Strategy config is invalid")
        self.status = StrategyStatus.ACTIVE
```

### Layer 2: Use Cases (Application Layer)

**Location**: `services/{service}/application/`

**Responsibility**:
- Application-specific business rules
- Orchestrate entities and repositories
- Define input/output ports

**Characteristics**:
- No knowledge of UI, frameworks, or databases
- Coordinates flow and execution of business rules
- Input/output through interfaces (ports)

```python
# Example use case (application layer)
class CreateStrategy:
    def __init__(
        self,
        strategy_repo: StrategyRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.strategy_repo = strategy_repo
        self.event_publisher = event_publisher
    
    def execute(self, command: CreateStrategyCommand) -> StrategyId:
        strategy = Strategy.create(
            user_id=command.user_id,
            name=command.name,
            config=command.config,
        )
        self.strategy_repo.save(strategy)
        self.event_publisher.publish(StrategyCreated(strategy.id))
        return strategy.id
```

### Layer 3: Interface Adapters (Infrastructure Layer)

**Location**: `services/{service}/adapters/`, `services/{service}/infrastructure/`

**Responsibility**:
- Convert data between external formats and internal formats
- Presenters format data for UI
- Controllers translate input to use case format
- Gateways implement interfaces for external services

**Characteristics**:
- No business logic
- Pure data transformation
- Keeps outer layers from affecting inner layers

```python
# Example adapter (infrastructure layer)
class ExchangeOrderGateway:
    def __init__(self, client: ExchangeClient) -> None:
        self.client = client
    
    def place_order(self, order: Order) -> ExchangeOrderId:
        response = self.client.submit_order(
            symbol=order.symbol.value,
            side=order.side.value,
            quantity=order.quantity,
            type=order.type.value,
        )
        return ExchangeOrderId(response['id'])
```

### Layer 4: Frameworks & Drivers (Interface Layer)

**Location**: External to core (web frameworks, databases, UI)

**Responsibility**:
- Handle external agencies
- Provide implementations for adapters
- Database, web server, UI

**Characteristics**:
- Changes rarely affect inner layers
- Glue code to make system work
- Multiple implementations possible

## Component Wiring

### Dependency Injection Container
```python
# infrastructure/container.py
class Container:
    def __init__(self) -> None:
        self._instances: dict[str, Any] = {}
    
    def resolve(self, protocol: type[T]) -> T:
        """Resolve dependency by protocol interface."""
        ...
    
    def register(self, protocol: type[T], implementation: T) -> None:
        """Register implementation for protocol."""
        ...
```

### Composition Root
Located in `src/quantx/main.py`:

```python
# Main composition root
def create_container() -> Container:
    container = Container()
    
    # Register repositories
    container.register(StrategyRepository, PostgresStrategyRepository())
    container.register(PositionRepository, MongoPositionRepository())
    
    # Register services
    container.register(ExchangeClient, BinanceExchangeAdapter())
    
    # Register use cases
    container.register(CreateStrategy, CreateStrategy(
        strategy_repo=container.resolve(StrategyRepository),
        event_publisher=container.resolve(EventPublisher),
    ))
    
    return container
```

## Cross-Cutting Concerns

### Logging
- Implemented in outer layer
- Structured logging passed inward
- No business logic knows about specific logger

### Security
- Authentication in interface layer
- Authorization checked before use cases
- Business rules focus on domain logic

### Caching
- Implemented as decorator in outer layer
- Transparent to inner layers
- Cache invalidation coordinated

### Transactions
- Managed by application layer
- Repository implementations handle transaction boundaries
- Unit of Work pattern for complex operations

## Package by Feature Structure

Each service follows Clean Architecture layers:

```
services/trading/
├── domain/                 # Layer 1: Entities
│   ├── entities/
│   ├── value_objects/
│   ├── services/
│   └── repositories/
│
├── application/            # Layer 2: Use Cases
│   ├── commands/
│   ├── queries/
│   ├── services/
│   └── dtos/
│
├── adapters/               # Layer 3: Interface Adapters
│   ├── inbound/
│   └── outbound/
│
└── infrastructure/         # Layer 4: Frameworks
    ├── config.py
    └── container.py
```

## Controller Pattern

Controllers act as entry points from outer layers:

```python
# adapters/inbound/http_controller.py
class TradingController:
    def __init__(self, create_strategy: CreateStrategy) -> None:
        self.create_strategy = create_strategy
    
    async def handle_create_strategy(self, request: Request) -> Response:
        command = CreateStrategyCommand(
            user_id=parse_user_id(request.headers),
            name=request.body['name'],
            config=StrategyConfig(**request.body['config']),
        )
        try:
            strategy_id = self.create_strategy.execute(command)
            return Response(status=201, body={'id': strategy_id})
        except ValidationError as e:
            return Response(status=400, body={'error': str(e)})
```

## Presenter Pattern

Presenters format data for specific interfaces:

```python
# adapters/outbound/telegram_presenter.py
class TelegramPresenter:
    def present_strategy(self, strategy: Strategy) -> str:
        return (
            f"Strategy: {strategy.name}\n"
            f"Type: {strategy.type.value}\n"
            f"Status: {strategy.status.value}\n"
            f"Positions: {len(strategy.positions)}"
        )
```

## Data Flow Examples

### Create Strategy Flow
```
1. Telegram Handler receives /create command
2. Controller creates CreateStrategyCommand
3. CreateStrategy use case validates and creates entity
4. Entity's business rules validate invariants
5. Repository persists to database
6. Event published to message queue
7. Presenter formats confirmation message
8. Telegram adapter sends response
```

### Execute Order Flow
```
1. Market data triggers signal evaluation
2. TradingSignalDetected event received
3. EvaluateSignal use case checks conditions
4. Order entity created with validated parameters
5. Exchange adapter places order via API
6. Execution result stored in database
7. Position aggregate updated
8. User notified via Telegram
```

## Testing Strategy

### Unit Tests (Entities)
- Test business rules in isolation
- No mocks, pure function tests
- Run in <1ms per test

### Unit Tests (Use Cases)
- Mock repositories and gateways
- Test orchestration logic
- Verify event publishing

### Integration Tests (Adapters)
- Test with real database
- Test with external API mocks
- Verify data transformation

### End-to-End Tests (Frameworks)
- Complete flow tests
- Real external API calls in sandbox
- Used sparingly due to cost

## Module Dependencies

### Allowed Dependencies
```
application → domain
adapters → application, domain
infrastructure → adapters, application, domain
frameworks → infrastructure, adapters
shared → (no dependencies - pure utilities)
```

### Forbidden Dependencies
- `domain` → `application` (violates dependency rule)
- `application` → `adapters` (breaks testability)
- Any layer → `frameworks` (prevents framework independence)

## Configuration Integration

Configuration flows through outer layers:

```python
# Outer layer provides config
class ConfigLoader:
    def load(self) -> AppConfig:
        return AppConfig(
            database_url=os.getenv('QUANTX_DATABASE_URL'),
            exchange_apis={...},
            risk_limits={...},
        )

# Inner layers receive config via DI
class RiskCalculationService:
    def __init__(self, config: RiskConfig) -> None:
        self.max_position_size = config.max_position_size
```

## Error Handling Across Layers

```
Framework Layer: HTTP response conversion
     ↓
Adapter Layer: Exception translation
     ↓
Application Layer: Business error handling
     ↓
Domain Layer: Domain-specific exceptions
```

```python
# Domain level
class InsufficientFundsError(DomainError): ...

# Application level
try:
    use_case.execute(command)
except InsufficientFundsError as e:
    raise ApplicationError("Trading halted", cause=e)

# Adapter level
try:
    response = self.exchange.place_order(order)
except ExchangeTimeout as e:
    raise InfrastructureError("Exchange unavailable", cause=e)

# Framework level
@app.exception_handler(InfrastructureError)
async def handle_infrastructure_error(request, exc):
    return JSONResponse(status_code=503, content={"error": "Service unavailable"})
```

## Related Documents
- [05_DOMAIN_MODEL.md](05_DOMAIN_MODEL.md)
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [08_DATABASE_DESIGN.md](08_DATABASE_DESIGN.md)
- [28_DEPENDENCY_INJECTION.md](28_DEPENDENCY_INTEGRATION.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Core Architecture*