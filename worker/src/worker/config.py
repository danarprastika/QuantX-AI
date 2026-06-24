"""Worker configuration using Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUANTX_WORKER_", env_file="../.env")

    broker_url: str = Field(default="amqp://quantx:quantx@localhost:5672//")
    result_backend: str = Field(default="redis://:quantx@localhost:6379/2")
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: list[str] = ["json"]
    timezone: str = "UTC"
    enable_utc: bool = True


def get_worker_settings() -> WorkerSettings:
    """Return worker settings."""
    return WorkerSettings()
