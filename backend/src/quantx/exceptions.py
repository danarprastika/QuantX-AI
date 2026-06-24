"""Exception handlers and custom exception types for QuantX API."""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class QuantXError(Exception):
    """Base exception for all QuantX errors."""

    def __init__(self, message: str, code: str = "internal_error") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class ConfigurationError(QuantXError):
    """Raised when configuration is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="configuration_error")


class InfrastructureError(QuantXError):
    """Raised when infrastructure is unavailable."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="infrastructure_error")


class AuthenticationError(QuantXError):
    """Raised when authentication fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="authentication_error")


def quantx_error_handler(request: Request, exc: QuantXError) -> JSONResponse:
    """Handle QuantXError exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": exc.code,
            "message": exc.message,
        },
    )


def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Request validation failed",
            "details": errors,
        },
    )


def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
        },
    )


def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""
    app.add_exception_handler(QuantXError, quantx_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
