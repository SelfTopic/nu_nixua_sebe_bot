import logging

from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ...callback import ClanRequestCallback
from ...config import settings
from ...exceptions import UserNotFoundError
from ...filters import ClanFilter, UserFilter
from ...services import UserService
from ...storage.clan_requests import pending_requests
from ...types import UserDTO

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(Command("register"), UserFilter())
async def register_to_clan(
    message: Message,
    user: UserDTO,
    user_service: UserService,
    command: CommandObject,
    bot: Bot,
) -> None:
    existing_user = await user_service.user_repository.get(by=user)

    if existing_user:
        await message.reply(
            f"Ты уже есть в клане под ником {existing_user.nickname}. "
            f"Чтобы изменить ник — используй /rename"
        )
        return

    nickname = command.args
    if not nickname:
        await message.reply("Используй как /register <твой ник в кс>")
        return

    pending_requests[user.id] = UserDTO(
        id=user.id,
        nickname=nickname,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
    )

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Принять ✅",
            callback_data=ClanRequestCallback(
                action="accept",
                telegram_id=user.id,
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Отклонить ❌",
            callback_data=ClanRequestCallback(
                action="reject",
                telegram_id=user.id,
            ).pack(),
        ),
    )

    await bot.send_message(
        chat_id=settings.CLAN_CHAT_ID,
        text=f"Запрос на вступление: {nickname} ({user_service.get_html_link_to_user(user)})",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )

    await message.reply("Запрос отправлен. Когда владелец отреагирует — я тебе сообщу.")


@router.message(Command("rename"), UserFilter(), ClanFilter())
async def rename_handler(
    message: Message,
    user: UserDTO,
    user_service: UserService,
    command: CommandObject,
) -> None:
    if not command.args:
        await message.reply("Используй как /rename <новый ник>")
        return

    existing = await user_service.user_repository.get(by=user)

    if not existing:
        raise UserNotFoundError()

    old_nickname = existing.nickname
    existing.nickname = command.args.strip()
    await user_service.user_repository.session.flush()

    await message.reply(f"Ник изменён: {old_nickname} → {existing.nickname} ✅")
