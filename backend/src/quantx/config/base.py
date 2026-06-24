"""Base configuration classes for QuantX AI."""

from enum import Enum
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUANTX_DATABASE_", env_file=".env")

    url: str = "postgresql+asyncpg://quantx:quantx@localhost:5432/quantx_db"
    echo: bool = False
    pool_size: int = Field(default=20, ge=1, le=100)
    max_overflow: int = Field(default=10, ge=0, le=50)


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUANTX_REDIS_", env_file=".env")

    url: str = "redis://:quantx@localhost:6379/0"
    max_connections: int = Field(default=50, ge=1, le=200)


class CelerySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUANTX_WORKER_", env_file=".env")

    broker_url: str = "amqp://quantx:quantx@localhost:5672//"
    result_backend: str = "redis://:quantx@localhost:6379/2"
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: List[str] = ["json"]
    timezone: str = "UTC"
    enable_utc: bool = True


class OpenTelemetrySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUANTX_OTEL_", env_file=".env")

    service_name: str = "quantx-api"
    service_version: str = "0.1.0"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUANTX_", env_file=".env", extra="ignore")

    env: Environment = Environment.DEVELOPMENT
    log_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    workers: int = Field(default=4, ge=1, le=64)
    secret_key: str = Field(default="change-me-in-production")
    allowed_hosts: List[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUANTX_", env_file=".env", extra="ignore")

    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()
    observability: OpenTelemetrySettings = OpenTelemetrySettings()


def get_settings() -> Settings:
    """Return the application settings singleton."""
    return Settings()


def validate_config() -> None:
    """Validate required configuration on startup."""
    settings = get_settings()
    required = [
        settings.database.url,
        settings.redis.url,
        settings.celery.broker_url,
    ]
    if not all(required):
        raise ValueError("Missing required configuration values")
