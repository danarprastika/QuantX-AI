# QuantX AI Commands

## Frontend (quantx-web)

```bash
cd apps/quantx-web

# Lint
npm run lint
npm run lint:fix

# Type check
npm run type-check

# Tests
npm run test
npm run test:coverage
npm run test:* (api-errors, rate-limits, logging-format, metrics-emission, web-vitals, error-display, correlation-flow, validation-errors, cache-invalidation, offline-cache, flag-targeting, sharia-flags, flag-fallback, locale-detection, rtl-layout, i18n-fallback)

# OpenAPI generation
npm run openapi:generate

# Quality checks
npm run check:error-boundaries
npm run check:cache-ttl
npm run check:externalized-strings
npm run check:lazy-loading

# Metrics
npm run metrics:web-vitals
npm run metrics:bundle-size
npm run trace:coverage
```