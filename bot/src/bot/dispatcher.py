"""Aiogram dispatcher setup for QuantX bot."""

import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.routers import common

logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    """Create and configure the dispatcher."""
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(common.router)

    @dp.error()
    async def global_error_handler(event: Any, exception: Exception) -> bool:
        logger.error("Unhandled bot error", exc_info=exception)
        return True

    return dp
