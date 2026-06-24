"""Dependency injection container for QuantX AI."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    """DI container for QuantX AI services."""

    config = providers.Configuration()

    database = providers.Singleton(None)
    cache = providers.Singleton(None)
    celery_app = providers.Singleton(None)


container = Container()
