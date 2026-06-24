"""Celery worker entrypoint for QuantX AI."""

import logging

from celery import Celery

from worker.config import get_worker_settings

logger = logging.getLogger(__name__)


def create_celery_app() -> Celery:
    """Create and configure the Celery application."""
    settings = get_worker_settings()

    app = Celery(
        "quantx-worker",
        broker=settings.broker_url,
        backend=settings.result_backend,
    )

    app.conf.update(
        task_serializer=settings.task_serializer,
        result_serializer=settings.result_serializer,
        accept_content=settings.accept_content,
        timezone=settings.timezone,
        enable_utc=settings.enable_utc,
        task_track_started=True,
        task_time_limit=3600,
        task_soft_time_limit=3300,
    )

    app.autodiscover_tasks(["worker.tasks"])

    logger.info("Celery app configured")
    return app


celery_app = create_celery_app()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    celery_app.start()
