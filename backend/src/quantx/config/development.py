"""Development environment configuration."""

from quantx.config.base import Settings


def get_settings() -> Settings:
    """Return development settings."""
    settings = Settings()
    settings.app.debug = True
    settings.app.log_level = "DEBUG"
    settings.database.echo = True
    return settings
