# QuantX AI - Kubernetes

## Overview

This document defines the Kubernetes deployment architecture for QuantX AI, including cluster design, service manifests, scaling policies, and operational procedures.

## Cluster Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Kubernetes Cluster Design                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │   Control    │  │   Control    │  │   Control    │  │   Control    │ │
│   │   Plane      │  │   Plane      │  │   Plane      │  │   Plane      │ │
│   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │   Worker     │  │   Worker     │  │   Worker     │                 │
│   │   Node       │  │   Node       │  │   Node       │                 │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│          │                 │                 │                         │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
│  │   Pods       │  │   Pods       │  │   Pods       │  │   Pods       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Namespace Organization
- `quantx-system` - Core services
- `quantx-user` - User-isolated resources
- `quantx-monitoring` - Observability
- `quantx-infra` - Infrastructure

## Deployment Manifest
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trading-service
  namespace: quantx-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: trading-service
  template:
    metadata:
      labels:
        app: trading-service
    spec:
      containers:
      - name: trading
        image: ghcr.io/quantx/trading-service:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: quantx-config
        - secretRef:
            name: quantx-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 10
```

## Related Documents
- [37_DEPLOYMENT.md](37_DEPLOYMENT.md)
- [38_DOCKER.md](38_DOCKER.md)
- [40_CI_CD.md](40_CI_CD.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Operations*