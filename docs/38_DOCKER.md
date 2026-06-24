# QuantX AI - Docker

## Overview

This document defines the Docker containerization strategy for QuantX AI services, including image optimization, multi-stage builds, security scanning, and registry management.

## Docker Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Docker Build Pipeline                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │   Source     │  │   Builder    │  │   Runtime    │                 │
│   │   Code       │  │   Stage      │  │   Stage      │                 │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│          │                 │                 │                         │
│   ┌──────▼────────────────────────────────────────────────────────┐    │
│   │                    Multi-Stage Dockerfile                         │    │
│   └─────────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Image      │  │   Registry   │  │   Scanner    │  │   Runtime    │ │
│  │   Build      │  │   (GHCR)     │  │   (Trivy)    │  │   (K8s)      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Multi-Stage Dockerfile

### Base Structure
```dockerfile
# syntax=docker/dockerfile:1.4

# Build stage
FROM python:3.11-slim as builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt && \
    pip install -r requirements.txt

# Runtime stage
FROM python:3.11-slim as runtime
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY src/ ./src/
COPY services/ ./services/

# Non-root user
RUN useradd -m -u 1000 quantx && \
    chown -R quantx:quantx /app
USER quantx

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

CMD ["python", "-m", "src.quantx.main"]
```

### Optimization Techniques
- Pin base image SHA hashes
- Multi-stage builds for smaller images
- .dockerignore for excluded files
- Layer caching optimization
- Non-root user for security

## Image Security

### Security Scanning
```yaml
# GitHub Actions security scan
- name: Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.REGISTRY }}/quantx/service:${{ github.sha }}
    format: sarif
    output: trivy-results.sarif
```

### Image Hardening
- Distroless base images (future)
- Read-only root filesystem
- Drop capabilities
- SecurityContext in Kubernetes

## Registry Management

### GitHub Container Registry
- Private registry
- Vulnerability scanning
- Image signing
- Lifecycle policies

### Tag Strategy
```
main-latest          # Latest main branch
main-{sha}           # Commit-based
v1.0.0               # Release tag
v1.0.0-rc.1          # Release candidate
```

## Related Documents
- [02_SYSTEM_ARCHITECTURE.md](02_SYSTEM_ARCHITECTURE.md)
- [39_KUBERNETES.md](39_KUBERNETES.md)
- [40_CI_CD.md](40_CI_CD.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Operations*