"""
Request ID middleware for correlation tracing.
"""

import uuid
from contextvars import ContextVar
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Generate and inject a unique request ID for correlation."""

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_ctx.set(request_id)

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def get_request_id() -> str | None:
    """Return the current request ID from context."""
    return request_id_ctx.get()
