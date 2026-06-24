"""Shared event types for QuantX AI."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class EventType(str, Enum):
    DOMAIN = "domain"
    INTEGRATION = "integration"


class BaseEvent(BaseModel):
    """Base event class."""

    event_id: str
    event_type: str
    occurred_at: datetime
    aggregate_id: str | None = None


class DomainEvent(BaseEvent):
    """Base class for domain events."""

    event_type: str = EventType.DOMAIN


class IntegrationEvent(BaseEvent):
    """Base class for integration events."""

    event_type: str = EventType.INTEGRATION
