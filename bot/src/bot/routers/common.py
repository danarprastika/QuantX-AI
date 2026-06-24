"""Common bot router with basic commands."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command."""
    await message.answer(
        "Welcome to QuantX AI!\n"
        "Your algorithmic trading companion.\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/ping - Check bot responsiveness"
    )


@router.message(Command("ping"))
async def cmd_ping(message: Message) -> None:
    """Handle /ping command."""
    await message.answer("Pong!")
