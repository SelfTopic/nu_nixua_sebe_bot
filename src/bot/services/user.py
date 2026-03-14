import logging

from aiogram.types import CallbackQuery, Message

from ..exceptions import UserNotFoundError
from ..repositories import UserRepository
from ..types import UserDTO
from .base import Base

logger = logging.getLogger(__name__)


class UserService(Base):
    """Сервис для управления сущностями User"""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

        logger.debug("User service initialize")
        return None

    # Текст ссылки на профиль пользователя внутри Telegram
    to_user_link = "tg://user?id={user_id}"

    # Текст ссылки на профиль пользователя вне Telegram
    to_profile_link = "https://t.me/{username}"

    @staticmethod
    def get_full_name(user: UserDTO) -> str:
        return (
            user.first_name + (" " + user.last_name if user.last_name else "")
        ).strip()

    @staticmethod
    def from_message(message: Message) -> UserDTO:

        user = message.from_user
        if not user:
            raise UserNotFoundError("User not found in aiogram.types.message")

        return UserDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )

    @staticmethod
    def from_callback(callback: CallbackQuery) -> UserDTO:

        user = callback.from_user

        return UserDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )

    def get_html_link_to_user(self, user: UserDTO) -> str:
        logger.debug("Method get_html_link_to_user called")

        full_name = self.get_full_name(user=user)
        link = f'<a href="{self.to_user_link.format(user_id=user.id)}">{full_name}</a>'

        logger.debug(f"Full name generated: {full_name}. Link={link}")
        return link

    def get_html_link_to_profile(self, user: UserDTO) -> str | None:
        logger.debug("Method get_html_link_to_profile called")
        if not user.username:
            logger.warning("Username is empty. Returning None")
            return None

        full_name = self.get_full_name(user=user)
        link = f'<a href="{self.to_profile_link.format(username=user.username)}">{full_name}</a>'

        logger.debug(f"Full name generated: {full_name}. Link={link}")
        return link
