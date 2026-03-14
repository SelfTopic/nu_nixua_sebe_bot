import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ...filters import UserFilter
from ...services import UserService
from ...types import UserDTO

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(
    CommandStart(),
    UserFilter(),
)
async def start_handler(
    message: Message,
    user: UserDTO,
    user_service: UserService,
) -> None:
    logger.debug(
        f"Start handling on start_handler. user={user}, user_service={user_service}"
    )

    user_mention = user_service.get_html_link_to_user(user)

    caption = f"Привет, {user_mention}, я ну нихуя себе бот. Я уникальный бот для клана (нихуя себе) на сервере CSSv34 'Тюрьма. Последняя надежда.'"
    existing_user = await user_service.user_repository.get(by=user)

    if not existing_user:
        caption += "\n\nТебя нет в моем списке участников клана. Напиши @chestor по поводу входа в клан или не используй меня. Все равно я тебе больше ни на что не отвечу."

    await message.reply(
        text=caption,
        parse_mode="HTML",
    )

    logger.debug("End handling on start_handler")
    return None
