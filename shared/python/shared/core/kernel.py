"""Core domain kernel with base classes."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Entity(BaseModel):
    """Base entity with identity."""

    id: str = Field(description="Unique identifier for the entity")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"frozen": False}


class ValueObject(BaseModel):
    """Immutable value object base class."""

    model_config = {"frozen": True}


class AggregateRoot(Entity):
    """Base aggregate root with domain events support."""

    _events: list[dict[str, Any]] = []

    def _register_event(self, event_name: str, event_data: dict[str, Any]) -> None:
        self._events.append({
            "name": event_name,
            "data": event_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def clear_events(self) -> None:
        self._events = []

    def get_events(self) -> list[dict[str, Any]]:
        return list(self._events)
