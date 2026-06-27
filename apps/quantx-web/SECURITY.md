# Security Policy

## Reporting Vulnerabilities

Report security vulnerabilities to security@quantx.ai. Do not create public issues.

## Security Standards

This frontend follows QuantX AI security standards per MDS Section 8:

- No secrets in client-side code
- HTTP-only cookies for authentication
- XSS prevention via React's built-in escaping
- CSP headers configured in Next.js
- WCAG 2.1 AA compliance (MDS Section 26)

## Dependency Security

- Dependencies scanned via Dependabot
- Critical vulnerabilities patched within 72 hours
- Lockfile committed for reproducible builds