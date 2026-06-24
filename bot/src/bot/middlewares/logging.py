"""Logging middleware for aiogram handlers."""

import logging
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class LoggingMiddleware(BaseMiddleware):
    """Log incoming Telegram updates."""

    async def __call__(self, handler, event: TelegramObject, data: dict) -> Any:
        logger = logging.getLogger(__name__)
        if isinstance(event, TelegramObject):
            logger.info("Received update: %s", event.model_dump())
        return await handler(event, data)
