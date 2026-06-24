"""Telegram bot entrypoint for QuantX AI."""

import asyncio
import logging
import signal
import sys
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import get_bot_settings
from bot.dispatcher import create_dispatcher
from bot.middlewares.logging import LoggingMiddleware


logger = logging.getLogger(__name__)


def _setup_signal_handlers(bot: Bot, dispatcher: Dispatcher) -> None:
    """Setup graceful shutdown signal handlers."""

    def shutdown() -> None:
        logger.info("Shutting down bot...")
        asyncio.ensure_future(bot.session.close())

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda s, f: shutdown())


async def main() -> None:
    """Main bot lifecycle."""
    settings = get_bot_settings()

    bot = Bot(
        token=settings.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dispatcher = create_dispatcher()
    dispatcher.message.middleware(LoggingMiddleware())

    _setup_signal_handlers(bot, dispatcher)

    logger.info("Starting bot polling...")
    await dispatcher.start_polling(
        bot,
        allowed_updates=["message", "callback_query"],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
