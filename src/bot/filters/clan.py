from typing import Any

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from ..services import UserService
from ..types import UserDTO


class ClanFilter(Filter):
    """Фильтр, пропускающий только участников клана."""

    async def __call__(
        self,
        message: Message | None = None,
        callback: CallbackQuery | None = None,
        **data: Any,
    ) -> bool:
        user_service: UserService = data["user_service"]
        user: UserDTO = data["user"]
        existing_user = await user_service.user_repository.get(by=user)
        return bool(existing_user)
