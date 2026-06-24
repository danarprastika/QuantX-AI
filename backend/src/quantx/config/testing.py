"""Testing environment configuration."""

from quantx.config.base import Settings


def get_settings() -> Settings:
    """Return testing settings."""
    settings = Settings()
    settings.app.env = "test"
    settings.app.debug = True
    settings.app.log_level = "WARNING"
    settings.database.url = "sqlite+aiosqlite:///:memory:"
    settings.database.echo = False
    settings.redis.url = "redis://localhost:6379/15"
    return settings
