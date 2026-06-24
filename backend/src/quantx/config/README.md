# Configuration Package

This package centralizes all application configuration using Pydantic Settings.

## Structure

- **base.py** - Base settings classes shared across all environments
- **development.py** - Development-specific overrides
- **production.py** - Production-specific overrides
- **testing.py** - Testing-specific overrides

## Environment Detection

The active environment is determined by `QUANTX_ENV`:
- `development`
- `staging`
- `production`
- `test`

## Usage

```python
from quantx.config import get_settings

settings = get_settings()
```
