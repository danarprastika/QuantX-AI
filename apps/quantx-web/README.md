# QuantX Web

Frontend web application for QuantX AI Enterprise Platform - Next.js with React.

## Features

- **API Integration**: OpenAPI 3.0 compliant client with error envelope handling
- **Observability**: Structured logging, metrics, and OpenTelemetry tracing
- **Error Handling**: Error boundaries with correlation ID propagation
- **Cache Management**: React Query with TTL-based expiration and namespaced keys
- **Feature Flags**: Client-side flag evaluation with Sharia Mode gating
- **Internationalization**: Arabic (RTL) and English support
- **Performance**: Core Web Vitals compliance, bundle budgets

## Development

```bash
npm install
npm run dev
```

## Quality Gates

```bash
npm run lint           # ESLint pass
npm run type-check     # TypeScript strict mode
npm run test           # Jest tests >=80% coverage
npm run check:error-boundaries  # Error boundary coverage
npm run check:cache-ttl         # Cache TTL validation
npm run check:externalized-strings  # i18n string check
npm run metrics:web-vitals        # Core Web Vitals
```

## Architecture

Follows Clean Architecture with DDD bounded contexts:
- `presentation/` - Next.js pages, components, layouts
- `application/` - API client layer, services
- `shared/` - Kernel, cache, flags, observability, i18n
- `infrastructure/` - External integrations
- `features/` - Feature-based modules

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API endpoint (default: /api/v1)
- `NEXT_PUBLIC_OTEL_ENDPOINT` - OpenTelemetry collector endpoint
- `NEXT_PUBLIC_LOG_LEVEL` - Logging level (default: info)