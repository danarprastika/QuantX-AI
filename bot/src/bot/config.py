"""Bot configuration using Pydantic Settings."""

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUANTX_BOT_", env_file="../.env")

    token: str = Field(min_length=1)
    admin_ids: List[int] = Field(default_factory=list)
    log_level: str = Field(
        default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )


def get_bot_settings() -> BotSettings:
    """Return bot settings."""
    return BotSettings()


def validate_config() -> None:
    """Validate required configuration on startup."""
    settings = get_bot_settings()
    if not settings.token or settings.token == "your_bot_token_here":
        raise ValueError("BOT_TOKEN is required")
