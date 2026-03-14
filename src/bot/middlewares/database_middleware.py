import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from ..database import sessionmaker

logger = logging.getLogger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    """Миддлварь, управляющий сессией базы данных"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        logger.debug("Databse middleware called")

        async with sessionmaker() as session:
            logger.debug("Session initialized")
            try:
                data["session"] = session
                await handler(event, data)
                await session.commit()
                logger.debug("Handler awaited, session commited")

            except Exception as E:
                await session.rollback()
                logger.error(f"Session rollback, Error: {E}")
                raise

        logger.debug("Session closed. End job")
