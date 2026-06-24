---
status: Approved
owner: Security Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/13_AUTHENTICATION.md
depends_on:
  - docs/07_SERVICE_BOUNDARIES.md
  - docs/14_AUTHORIZATION.md
  - docs/27_CONFIGURATION.md
related_documents:
  - docs/07_SERVICE_BOUNDARIES.md
  - docs/14_AUTHORIZATION.md
  - docs/27_CONFIGURATION.md
---
# QuantX AI - Authentication

## Overview

This document defines the authentication architecture for QuantX AI, including user identification, token management, multi-factor authentication, and session handling.

## Authentication Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Authentication Flow                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│   │   Client     │    │   API        │    │   Auth       │             │
│   │              │───▶│   Gateway    │───▶│   Service    │             │
│   └──────────────┘    └──────┬───────┘    └──────┬───────┘             │
│                            │                 │                     │
│                     ┌──────▼───────┐    ┌────▼──────┐             │
│                     │   JWT        │    │   User    │             │
│                     │   Validator   │    │ Repository│             │
│                     └──────┬───────┘    └────┬──────┘             │
│                            │                 │                     │
│                            ▼                 ▼                     │
│                   ┌────────────────┐  ┌────────────────┐            │
│                   │   Authorized   │  │   User Found   │            │
│                   │   Response     │  │   Response     │            │
│                   └────────────────┘  └────────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
```

## Authentication Methods

### Primary: Telegram-based Authentication
Users authenticate via their Telegram account:
1. User sends `/start` command to bot
2. Telegram ID stored as unique identifier
3. JWT token generated and cached
4. Token refreshed automatically

**Rationale**:
- No password management overhead
- Familiar flow for target audience
- Built-in 2FA (Telegram security)
- Eliminates account recovery complexity

**Alternatives Considered**:
- Email/password: Higher operational overhead, security concerns
- OAuth providers: Third-party dependency, complexity
- API keys only: Not user-friendly for end users

### Secondary: JWT Token Authentication
For API clients and programmatic access:
1. Obtain token via `/auth/login` with Telegram ID
2. Token cached in HttpOnly secure cookie
3. Automatic refresh on expiry

### API Key Authentication (Future)
For algorithmic trading:
1. Generate API key via UI
2. Key stored encrypted
3. HMAC signature on requests

## Token Management

### JWT Token Structure
```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user-uuid",
  "tid": "telegram-id",
  "iat": 1704067200,
  "exp": 1704068100,
  "tier": "premium",
  "jti": "unique-jwt-id"
}

Signature: HMAC-SHA256(base64(header) + "." + base64(payload), secret)
```

### Token Types

#### Access Token
- **Lifespan**: 15 minutes
- **Scope**: All authenticated endpoints
- **Storage**: Memory only, refreshed silently

#### Refresh Token
- **Lifespan**: 7 days
- **Scope**: Token refresh endpoint only
- **Storage**: HttpOnly secure cookie

### Token Refresh Flow
```
1. Client detects 401 response
2. Call /auth/refresh with refresh token
3. Validate refresh token
4. Issue new access token
5. Return in response body
```

### Refresh Endpoint
```http
POST /api/v1/auth/refresh
Cookie: refresh_token=<token>
```

**Response**:
```json
{
  "access_token": "<new-jwt>",
  "expires_in": 900,
  "token_type": "Bearer"
}
```

## Session Management

### Session Storage
- Redis with TTL (24 hours)
- FSM context serialized
- Per-user session isolation

### Session Schema
```redis
session:{telegram_id} = {
  "state": "selecting_symbol",
  "context": {
    "strategy_data": {...},
    "step": 2,
    "started_at": "timestamp"
  },
  "expires_at": "timestamp"
}
```

### Session Cleanup
- Automatic TTL expiration
- Manual cleanup on /reset command
- Activity-based refresh

## Multi-Factor Authentication

### Current State
- Telegram account serves as MFA
- Bot token tied to Telegram session
- No additional MFA required

### Future MFA Options
| Method | Status | Reason |
|--------|--------|--------|
| TOTP | Planned | Time-based codes |
| SMS | Considered | Phone verification |
| Email | Considered | Email verification |
| Hardware | Rejected | Too burdensome |

## Authentication Flow

### Login Flow (Telegram)
```
1. User: /start @bot
2. Bot: Receives Telegram ID
3. Service: Find or create user
4. Service: Generate JWT tokens
5. Service: Cache refresh token
6. Service: Return tokens to client
7. Bot: Store access token in session
```

### API Request Auth
```
1. Client: Include Authorization header
2. Gateway: Extract Bearer token
3. Validator: Verify JWT signature
4. Validator: Check expiration
5. Validator: Extract user claims
6. Gateway: Add user context to request
7. Service: Process authenticated request
```

### Token Validation
```python
def validate_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
        )
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
```

## Security Considerations

### Token Storage
- Access tokens: Memory only, never stored
- Refresh tokens: HttpOnly, secure, SameSite cookies
- No token in localStorage/sessionStorage

### Token Rotation
- New refresh token on each refresh
- Old refresh token invalidated
- Single refresh token per user

### Token Revocation
- Store revoked JTI in Redis with expiry
- Check revocation on refresh
- Immediate invalidation on logout

### Logout Flow
```
1. Client calls /auth/logout
2. Service adds JTI to revocation list
3. Delete refresh token cookie
4. Clear session cache
```

## Rate Limiting

### Auth Endpoints
| Endpoint | Limit | Window | Per |
|----------|-------|--------|-----|
| /register | 10 | 1h | IP |
| /login | 20 | 1h | IP |
| /refresh | 100 | 1h | User |

### Brute Force Protection
- Account lockout after 5 failed attempts
- Progressive delays (1s, 2s, 4s, 8s)
- Email notification on lockout

## Token Claims

### Standard Claims
| Claim | Description | Source |
|-------|-------------|--------|
| sub | User UUID | Database |
| tid | Telegram ID | Telegram |
| iat | Issued at | JWT generation |
| exp | Expires at | JWT generation |
| tier | Subscription tier | Database |
| jti | Unique token ID | UUID generation |

### Custom Claims
| Claim | Description | Used For |
|-------|-------------|----------|
| scopes | Permission scopes | Authorization |
| exchanges | Connected exchanges | Trading access |

## Refresh Token Schema
```sql
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    token_hash VARCHAR(64) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    
    UNIQUE(user_id, token_hash)
);
```

## Related Documents
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [14_AUTHORIZATION.md](14_AUTHORIZATION.md)
- [27_CONFIGURATION.md](27_CONFIGURATION.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Security Team*
*Source of Truth: docs/13_AUTHENTICATION.md*
*Depends On: 07_SERVICE_BOUNDARIES.md, 14_AUTHORIZATION.md, 27_CONFIGURATION.md*
*Related Documents: 07_SERVICE_BOUNDARIES.md, 14_AUTHORIZATION.md, 27_CONFIGURATION.md*
*Phase: Infrastructure*
