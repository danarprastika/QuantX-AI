"""Configuration schemas for QuantX AI."""

from enum import Enum

from pydantic import BaseModel


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class BaseServiceConfig(BaseModel):
    """Base configuration for all services."""

    environment: Environment = Environment.DEVELOPMENT
    log_level: str = "INFO"
