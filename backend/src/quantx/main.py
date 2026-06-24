"""FastAPI application entry point for QuantX API."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from quantx.config import get_settings
from quantx.exceptions import register_exception_handlers
from quantx.logging import configure_logging
from quantx.middleware.security import SecurityHeadersMiddleware
from quantx.middleware.request_id import RequestIdMiddleware
from quantx.observability import configure_tracing, shutdown_tracing
from quantx.health.routes import router as health_router

settings = get_settings()


def create_app() -> FastAPI:
    """Application factory for creating and configuring the FastAPI app."""
    configure_logging(settings.app.log_level)
    configure_tracing(
        service_name=settings.observability.service_name,
        service_version=settings.observability.service_version,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            shutdown_tracing()

    app = FastAPI(
        title="QuantX API",
        description="QuantX AI Algorithmic Trading Platform API",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestIdMiddleware)

    register_exception_handlers(app)

    app.include_router(health_router, prefix="", tags=["health"])

    @app.get("/")
    async def root() -> dict:
        return {"service": "quantx-api", "version": "0.1.0"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "quantx.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.debug,
        log_level=settings.app.log_level.lower(),
    )
