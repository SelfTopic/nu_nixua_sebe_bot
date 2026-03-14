from typing import Any

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories import UserRepository
from ..services import UserService


class UserFilter(Filter):
    """Фильтр, прокидывающий сервис UserService в хэндлеры"""

    async def __call__(
        self,
        message: Message | None = None,
        callback: CallbackQuery | None = None,
        **data: Any,
    ) -> bool | dict[str, Any]:

        session: AsyncSession = data["session"]

        user_repo = UserRepository(session=session)
        user_service = UserService(user_repository=user_repo)

        if message:
            if not message.from_user:
                return False
            user = user_service.from_message(message)

        elif callback:
            if not callback.from_user:
                return False
            user = user_service.from_callback(callback)

        else:
            return False

        return {"user": user, "user_service": user_service}
