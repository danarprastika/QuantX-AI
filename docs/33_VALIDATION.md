---
status: Approved
owner: Backend Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/33_VALIDATION.md
depends_on:
  - docs/12_API_CONTRACTS.md
  - docs/32_ERROR_HANDLING.md
related_documents:
  - docs/12_API_CONTRACTS.md
  - docs/32_ERROR_HANDLING.md
---
# QuantX AI - Validation

## Overview

This document defines the validation architecture for QuantX AI, including input validation, business rule validation, data integrity checks, and validation frameworks.

## Validation Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Validation Pipeline                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │   Request    │  │   Business   │  │   External   │  │   Data       │ │
│   │   Schema     │  │   Rules      │  │   Format     │  │   Integrity   │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼─────────────────────────────────────────────────────────────┐    │
│   │                    Validation Engine                                │    │
│   │  Applies all validation rules, collects errors                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Reject     │  │   Sanitize   │  │   Transform  │  │   Accept     │ │
│  │   Request    │  │   Input      │  │   Data       │  │   Request    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Validation Framework

### Pydantic Models
```python
class StrategyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    symbol: Symbol
    timeframe: Timeframe
    config: StrategyConfig
    
    @validator("symbol")
    def validate_symbol(cls, v):
        if not EXCHANGE_SYMBOLS.is_valid(v):
            raise ValueError("Invalid trading symbol")
        return v

class PositionClose(BaseModel):
    quantity: Decimal = Field(..., gt=0)
    
    @root_validator
    def validate_quantity(cls, values):
        if values["quantity"] > position.remaining_quantity:
            raise ValueError("Cannot close more than position size")
        return values
```

## Business Rule Validation

### Strategy Limits
```python
def validate_strategy_limits(
    user_id: UserId,
    config: StrategyConfig,
) -> ValidationResult:
    user = user_repo.get(user_id)
    tier = get_tier_limits(user.subscription_tier)
    
    errors = []
    if config.risk_limit > tier.max_risk_limit:
        errors.append(f"Risk limit exceeds {tier.max_risk_limit}")
    
    active_strategies = strategy_repo.count_active(user_id)
    if active_strategies >= tier.max_strategies:
        errors.append(f"Max strategies ({tier.max_strategies}) reached")
    
    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
    )
```

## Related Documents
- [12_API_CONTRACTS.md](12_API_CONTRACTS.md)
- [32_ERROR_HANDLING.md](32_ERROR_HANDLING.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Backend Team*
*Source of Truth: docs/33_VALIDATION.md*
*Depends On: 12_API_CONTRACTS.md, 32_ERROR_HANDLING.md*
*Related Documents: 12_API_CONTRACTS.md, 32_ERROR_HANDLING.md*
*Phase: Infrastructure*
