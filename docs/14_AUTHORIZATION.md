# QuantX AI - Authorization

## Overview

This document defines the authorization architecture for QuantX AI, including permission models, role-based access control, policy enforcement, and resource-level permissions.

## Authorization Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Authorization Flow                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│   │   Request    │    │   Policy     │    │   Permission │               │
│   │   Context    │───▶│   Engine     │───▶│   Checker    │               │
│   └──────────────┘    └──────┬───────┘    └──────┬───────┘               │
│                            │                 │                       │
│                     ┌──────▼───────┐    ┌────▼──────┐               │
│                     │   Role      │    │   Resource│               │
│                     │   Resolver   │    │   Owner   │               │
│                     └──────┬───────┘    └────┬──────┘               │
│                            │                 │                       │
│                            ▼                 ▼                       │
│                   ┌────────────────┐  ┌────────────────┐              │
│                   │   Allowed    │  │   Owner Check   │              │
│                   │   Response   │  │   Response     │              │
│                   └────────────────┘  └────────────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
```

## Permission Model

### Role-Based Access Control (RBAC)

| Role | Create Strategy | Activate Strategy | Place Orders | Cancel Orders | View Analytics | Admin Access |
|------|-----------------|-------------------|--------------|---------------|----------------|--------------|
| Free | ✓ (1 max) | ✓ | ✓ (small qty) | ✓ | Limited | ✗ |
| Basic | ✓ (5 max) | ✓ | ✓ | ✓ | Full | ✗ |
| Premium | ✓ (unlimited) | ✓ | ✓ (full) | ✓ | Full | ✗ |
| Enterprise | ✓ (unlimited) | ✓ | ✓ (full) | ✓ | Full | Partial |
| Admin | ✓ | ✓ | ✓ | ✓ | Full | Full |

### Permission Hierarchy
```
Admin (all permissions)
    ↓
Enterprise (all except admin)
    ↓
Premium (full trading)
    ↓
Basic (limited strategies)
    ↓
Free (minimal)
```

## Resource Ownership

### Ownership Rules
1. **Users own Strategies** - User can only manage their own strategies
2. **Strategies own Positions** - Positions linked to strategy's user
3. **Strategies own Orders** - Orders linked to position's strategy
4. **Users own API Keys** - User can only manage their own keys

### Ownership Validation
```python
def can_access_user_resource(user_id: UserId, resource_user_id: UserId) -> bool:
    """Check if user owns the resource."""
    return user_id == resource_user_id

def can_access_strategy_resource(
    user_id: UserId, 
    strategy_id: StrategyId,
) -> bool:
    """Check if user owns the strategy."""
    strategy = strategy_repo.get(strategy_id)
    return strategy.user_id == user_id
```

## Policy Enforcement Points

### API Gateway Level
```python
# Authorization middleware
async def authz_middleware(
    request: Request,
    call_next: Callable,
) -> Response:
    user = request.state.user
    endpoint = request.url.path
    method = request.method
    
    # Check subscription tier
    if not check_tier_permission(user.tier, endpoint):
        return JSONResponse(
            status_code=403,
            content={"error": "upgrade_required"}
        )
    
    return await call_next(request)
```

### Service Level
```python
# Service authorization
async def activate_strategy(
    user_id: UserId,
    strategy_id: StrategyId,
) -> None:
    # Check ownership
    strategy = await strategy_repo.get(strategy_id)
    if strategy.user_id != user_id:
        raise AuthorizationError("Cannot access other user's strategy")
    
    # Check tier limits
    active_count = await strategy_repo.count_active_strategies(user_id)
    tier_limits = get_tier_limits(user.tier)
    if active_count >= tier_limits.max_active_strategies:
        raise TierLimitError("Exceeds active strategy limit")
```

## Subscription-Based Authorization

### Tier Limits
| Tier | Max Active Strategies | Max Positions | Daily Order Limit | API Rate Limit |
|------|-----------------------|-------------|-------------------|----------------|
| Free | 1 | 5 | 50 | 100/min |
| Basic | 5 | 20 | 200 | 500/min |
| Premium | Unlimited | 100 | Unlimited | 2000/min |
| Enterprise | Unlimited | Unlimited | Unlimited | 10000/min |

### Tier Check Implementation
```python
class TierAuthorization:
    def __init__(self, subscription_service: SubscriptionService) -> None:
        self.subscription_service = subscription_service
    
    async def check_strategy_limit(self, user_id: UserId) -> bool:
        tier = await self.subscription_service.get_tier(user_id)
        active_count = await self.strategy_service.count_active(user_id)
        return active_count < self.tier_limits[tier].max_strategies
```

## Exchange Authorization

### Exchange Credentials
- Stored encrypted per user
- Read-only for strategies
- Write access through trading service only
- No direct API key exposure

### Exchange Permission Rules
1. User must have credentials for exchange
2. Strategy must use user's exchange account
3. Orders limited to connected exchanges
4. Withdrawal operations prohibited

## Action-based Permissions

### Strategy Actions
| Action | Free | Basic | Premium | Enterprise |
|--------|------|-------|---------|------------|
| Create | ✓ (1) | ✓ (5) | ✓ | ✓ |
| Read | ✓ | ✓ | ✓ | ✓ |
| Update | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) |
| Delete | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) |
| Activate | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) |
| Deactivate | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) |
| Backtest | ✓ (limited) | ✓ | ✓ | ✓ |

### Trading Actions
| Action | Free | Basic | Premium | Enterprise |
|--------|------|-------|---------|------------|
| View Positions | ✓ | ✓ | ✓ | ✓ |
| View Orders | ✓ | ✓ | ✓ | ✓ |
| Place Order | ✓ (small) | ✓ | ✓ | ✓ |
| Cancel Order | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) |
| Modify Order | ✗ | ✗ | ✓ | ✓ |

## Scope-based Authorization

### JWT Scopes
```
scopes: [
  "strategy:read",
  "strategy:create",
  "strategy:update:own",
  "strategy:delete:own",
  "trading:positions:read",
  "trading:orders:create",
  "trading:orders:cancel:own"
]
```

### Scope Checking
```python
def check_scope(required: str, scopes: list[str]) -> bool:
    """Check if required scope is in allowed scopes."""
    if "*" in scopes:
        return True
    return required in scopes

# Check ownership in scope
def can_update_strategy(
    user_scopes: list[str],
    user_id: UserId,
    strategy_user_id: UserId,
) -> bool:
    owns = user_id == strategy_user_id
    has_update_scope = "strategy:update" in user_scopes
    has_own_scope = "strategy:update:own" in user_scopes and owns
    
    return has_update_scope or has_own_scope
```

## Admin Authorization

### Admin Capabilities
- View all users
- Modify user subscription tiers
- System configuration changes
- Emergency strategy shutdown
- Audit log access

### Admin Role Assignment
- Manual assignment by system
- Cannot self-assign
- Logged on every admin action
- Requires special authentication flow

## Authorization Decisions Matrix

| User ID | Resource ID | Action | Decision | Reason |
|---------|-------------|--------|----------|--------|
| Match | Match | Any | Allow | Owner |
| Match | Mismatch | Own-only | Deny | Not owner |
| Match | Match | Admin-only | Deny | Not admin |
| Admin | Any | Any | Allow | Admin role |
| Expired | Any | Any | Deny | Subscription expired |

## Error Handling

### Authorization Errors
```json
{
  "error": {
    "code": "AUTHORIZATION_FAILED",
    "message": "Insufficient permissions",
    "details": {
      "required": "strategy:activate",
      "user_tier": "free",
      "resource_owner": "other_user"
    ],
    "correlation_id": "uuid"
  }
}
```

### Tier Limit Errors
```json
{
  "error": {
    "code": "TIER_LIMIT_EXCEEDED",
    "message": "You have exceeded your plan limits",
    "details": {
      "limit": "max_active_strategies",
      "current": 1,
      "allowed": 1,
      "upgrade_url": "https://quantx.ai/pricing"
    }
  }
}
```

## Caching Authorization Decisions

### Cache Strategy
- User permissions cached for 5 minutes
- Tier limits cached for 1 hour
- No caching for admin operations
- Cache invalidated on subscription change

### Cache Key Format
```
authz:user:{user_id}:permissions
authz:user:{user_id}:tier
authz:strategy:{strategy_id}:ownership
```

## Related Documents
- [13_AUTHENTICATION.md](13_AUTHENTICATION.md)
- [15_SECURITY.md](15_SECURITY.md)
- [55_NON_FUNCTIONAL_REQUIREMENTS.md](55_NON_FUNCTIONAL_REQUIREMENTS.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Infrastructure*