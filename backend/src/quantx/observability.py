"""Observability module: logging, metrics, and tracing setup."""

import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Histogram
from structlog.types import EventDict, WrappedLogger


HTTP_REQUESTS_TOTAL = Counter(
    "quantx_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION = Histogram(
    "quantx_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

CELERY_TASKS_TOTAL = Counter(
    "quantx_celery_tasks_total",
    "Total Celery tasks processed",
    ["task_name", "status"],
)

CELERY_TASK_DURATION = Histogram(
    "quantx_celery_task_duration_seconds",
    "Celery task duration in seconds",
    ["task_name"],
)


def configure_logging(log_level: str = "INFO") -> None:
    """Configure structured logging for the application."""
    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    handler = logging.StreamHandler(sys.stdout)
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(),
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())


def get_logger(name: str) -> structlog.BoundLogger:
    """Return a structured logger instance."""
    return structlog.get_logger(name)


def _add_request_context(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add request-specific context to log records."""
    event_dict["service"] = "quantx-api"
    event_dict["environment"] = "development"
    return event_dict


def configure_tracing(service_name: str, service_version: str) -> None:
    """Configure OpenTelemetry distributed tracing."""
    provider = trace.get_tracer_provider()
    if provider is None or not hasattr(provider, "add_span_processor"):
        resource = Resource.create({
            "service.name": service_name,
            "service.version": service_version,
        })
        provider = TracerProvider(resource=resource)
        processor = BatchSpanProcessor(
            OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
        )
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)


def shutdown_tracing() -> None:
    """Shutdown the tracing provider."""
    provider = trace.get_tracer_provider()
    if hasattr(provider, "shutdown"):
        provider.shutdown()


@asynccontextmanager
async def lifespan_tracing() -> AsyncIterator[None]:
    """Async context manager for tracing lifecycle."""
    try:
        yield
    finally:
        shutdown_tracing()
