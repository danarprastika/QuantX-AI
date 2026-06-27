# Contributing to QuantX Web

## Development Setup

```bash
cd apps/quantx-web
npm install
npm run dev
```

## Code Standards

- Follow MDS naming conventions (Section 13)
- TypeScript strict mode required
- ESLint with no warnings
- WCAG 2.1 AA accessibility for all components

## Testing

```bash
npm run test          # Run tests
npm run test:coverage # With coverage report
npm run lint          # Code linting
npm run type-check    # TypeScript validation
```

## Quality Gates

All code must pass before merge:
- Lint: `npm run lint`
- Type-check: `npm run type-check`
- Tests: `npm run test:coverage` (≥80%)
- Accessibility: axe-core testing per MDS 26