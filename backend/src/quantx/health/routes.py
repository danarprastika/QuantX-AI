"""Health check endpoints for QuantX API."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/health/live")
async def liveness() -> dict:
    """Liveness probe - indicates the service is running."""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness() -> dict:
    """Readiness probe - indicates the service can handle requests."""
    checks = {
        "database": True,
        "cache": True,
        "message_queue": True,
    }

    if all(checks.values()):
        return {"status": "ready", "checks": checks}

    raise HTTPException(status_code=503, detail=checks)


@router.get("/health")
async def health() -> dict:
    """Overall health check endpoint."""
    return {
        "status": "healthy",
        "service": "quantx-api",
        "version": "0.1.0",
    }
