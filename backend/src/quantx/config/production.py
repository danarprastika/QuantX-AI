"""Production environment configuration."""

from quantx.config.base import Settings


def get_settings() -> Settings:
    """Return production settings."""
    settings = Settings()
    settings.app.env = "production"
    settings.app.debug = False
    settings.app.log_level = "INFO"
    settings.app.workers = 8
    settings.database.echo = False
    return settings
