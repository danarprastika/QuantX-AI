# QuantX Web Architecture

## Overview

This document describes the architecture of the QuantX Web frontend application.

## Technology Stack

- **Framework**: Next.js (Current Stable) with React (Current Stable)
- **Language**: TypeScript (Strict Mode)
- **Styling**: Tailwind CSS with RTL plugin
- **State Management**: React Query (TanStack Query)
- **Observability**: OpenTelemetry Browser SDK
- **Testing**: Jest, Playwright, axe-core

## Architecture Layers

### Presentation Layer (`src/presentation/`)

- **pages/** - Next.js route pages with error boundaries per MDS Section 51
- **components/** - Reusable UI components following pattern library
- **layouts/** - RTL-aware page layouts
- **hooks/** - Custom React hooks

### Application Layer (`src/application/`)

- **api/client.ts** - Base API client consuming OpenAPI spec
- **api/endpoints/** - Generated endpoint clients
- **services/** - Client-side services

### Shared Layer (`src/shared/`)

- **kernel/** - Error types, quantx.exception.ts
- **i18n/** - Internationalization with Arabic RTL support
- **cache/** - React Query configuration, cache hooks
- **flags/** - Feature flag client with naming conventions
- **observability/** - Logging, metrics, tracing

### Infrastructure Layer (`src/infrastructure/`)

- **telemetry/** - OpenTelemetry browser setup
- **storage/** - LocalStorage, IndexedDB wrappers

### Features Layer (`src/features/`)

- **market-intelligence/** - Market data and signals feature module
- **trading-signals/** - Trading signal generation and display
- **portfolio/** - Portfolio management and optimization
- **risk-management/** - Risk assessment and controls
- **sharia-compliance/** - Sharia Mode features

## Quality Gates

All code must pass:
- WCAG 2.1 AA accessibility (axe-core)
- TypeScript strict mode
- ESLint with no warnings
- Jest coverage >= 80%
- Core Web Vitals targets (LCP < 2.5s, FID < 100ms, CLS < 0.1)

## API Governance

- Versioned API paths: `/api/v{version}/{resource}`
- Standardized error envelope handling
- Rate limiting with exponential backoff
- Idempotency key support for write operations