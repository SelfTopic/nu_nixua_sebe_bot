import logging

from aiogram import Router
from aiogram.types import ErrorEvent

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.errors()
async def my_error_handler(event: ErrorEvent):
    logger.exception(
        f"Cause unexpected exception: {event.exception}",
    )
    try:
        if event.update.message and event.bot:
            await event.bot.send_message(
                chat_id=event.update.message.chat.id,
                text=f"Error: {event.exception}",
            )
    except Exception as e:
        logger.error(f"Failed to send error message to user: {e}")
