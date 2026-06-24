# QuantX AI - Configuration

## Overview

This document defines the configuration management architecture for QuantX AI, including environment variables, configuration sources, validation, and secret management.

## Configuration Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Configuration Sources                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │ Environment  │  │   Config     │  │ HashiCorp    │  │    YAML/     │ │
│   │   Variables  │  │   Maps       │  │   Vault      │  │   JSON       │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼─────────────────────────────────────────────────────────────┐    │
│   │                    Configuration Service                              │    │
│   │  Validates, merges, and serves configuration                        │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Strategy   │  │   Trading    │  │   Market     │  │   User       │ │
│  │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Configuration Sources (Priority Order)

### 1. Environment Variables (Highest Priority)
- Direct override capability
- Deployment-specific values
- Secrets (via reference)
- Format: `QUANTX_{SERVICE}_{KEY}`

### 2. Configuration Maps
- Kubernetes ConfigMap
- Service-specific settings
- Feature flags
- Default values

### 3. HashiCorp Vault (Secrets)
- Database credentials
- API keys
- TLS certificates
- Dynamic secrets

### 4. Configuration Files (Lowest Priority)
- `config.yaml` for defaults
- JSON for structured config
- Version controlled
- Documentation

## Environment Variables

### Core Configuration
```
QUANTX_ENV=production
QUANTX_SERVICE_NAME=trading-service
QUANTX_LOG_LEVEL=INFO
QUANTX_METRICS_PORT=9090
```

### Database Configuration
```
QUANTX_DATABASE_URL=postgresql://...
QUANTX_REDIS_URL=redis://...
QUANTX_RABBITMQ_URL=amqp://...
QUANTX_MONGODB_URL=mongodb://...
```

### Exchange Configuration
```
QUANTX_EXCHANGE_BINANCE_API_KEY=secure://vault/binance-key
QUANTX_EXCHANGE_BINANCE_API_SECRET=secure://vault/binance-secret
QUANTX_EXCHANGE_COINBASE_API_KEY=secure://vault/coinbase-key
```

### Feature Flags
```
QUANTX_FEATURE_NEW_PREDICTOR=true
QUANTX_FEATURE_ENSURE_RISK_CONTROLS=true
QUANTX_FEATURE_BACKTESTING=true
```

## Configuration Schema

### Pydantic Settings
```python
class DatabaseConfig(BaseSettings):
    url: PostgresDsn
    pool_min: int = 20
    pool_max: int = 100
    echo: bool = False
    
    class Config:
        env_prefix = "QUANTX_DATABASE_"

class ExchangeConfig(BaseSettings):
    binance_api_key: SecretStr
    binance_api_secret: SecretStr
    rate_limit: int = 1200
    
    class Config:
        env_prefix = "QUANTX_EXCHANGE_"

class AppConfig(BaseSettings):
    env: Environment = Environment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO
    database: DatabaseConfig = DatabaseConfig()
    exchange: ExchangeConfig = ExchangeConfig()
    
    class Config:
        env_prefix = "QUANTX_"
        env_file = ".env"
```

## Secret Management

### Vault Integration
```python
class VaultSecretProvider:
    def __init__(self, vault_url: str, token: str) -> None:
        self.client = hvac.Client(url=vault_url, token=token)
    
    def get_secret(self, path: str) -> SecretStr:
        """Retrieve secret from Vault."""
        secret = self.client.secrets.kv.v2.read_secret_version(path=path)
        return SecretStr(secret['data']['data']['value'])
```

### Secret Rotation
- Database passwords: 90 days
- API keys: Manual (user-managed)
- TLS certificates: 30 days before expiry
- JWT secrets: 180 days

## Feature Flags

### Flag Configuration
```python
class FeatureFlags:
    def __init__(self, config: AppConfig) -> None:
        self.flags = {
            "new_predictor": config.get("feature.new_predictor", False),
            "backtesting": config.get("feature.backtesting", True),
            "risk_controls": config.get("feature.risk_controls", True),
        }
    
    def is_enabled(self, flag: str) -> bool:
        return self.flags.get(flag, False)
```

### Flag Sources
- Environment variables: `QUANTX_FEATURE_*`
- Database: User-configurable flags
- Vault: Admin-only flags
- Remote config: Unlaunch/Flipt (future)

## Configuration Validation

### Startup Validation
```python
def validate_config(config: AppConfig) -> None:
    """Validate configuration on startup."""
    required = [
        config.database.url,
        config.redis.url,
        config.exchange.binance_api_key,
    ]
    
    missing = [r for r in required if not r]
    if missing:
        raise ConfigurationError(f"Missing required config: {missing}")
    
    # Validate ranges
    if config.database.pool_max < config.database.pool_min:
        raise ConfigurationError("Pool max must be >= pool min")
```

### Runtime Validation
- Health check endpoint
- Config change notifications
- Drift detection
- Alert on invalid config usage

## Configuration Versioning

### Version Format
Semantic versioning: MAJOR.MINOR.PATCH

### Change Types
- **MAJOR**: Breaking changes, removal
- **MINOR**: New fields, defaults changed
- **PATCH**: Documentation, comments

## Related Documents
- [28_DEPENDENCY_INJECTION.md](28_DEPENDENCY_INJECTION.md)
- [45_PROJECT_CONVENTIONS.md](45_PROJECT_CONVENTIONS.md)
- [43_CODING_STANDARD.md](43_CODING_STANDARD.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Infrastructure*