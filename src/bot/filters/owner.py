from typing import Any

from aiogram.filters import Filter
from aiogram.types import Message

from ..config import settings


class OwnerFilter(Filter):
    """Фильтр, пропускающий только владельца клана."""

    async def __call__(
        self,
        message: Message,
    ) -> bool | dict[str, Any]:

        if not message.from_user:
            return False

        if message.from_user.id != settings.OWNER_TELEGRAM_ID:
            return False

        return True
