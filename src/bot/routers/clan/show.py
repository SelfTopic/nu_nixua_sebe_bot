import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ...filters import ClanFilter, UserFilter
from ...services import UserService
from ...types import UserDTO

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(
    Command("all"),
    UserFilter(),
    ClanFilter(),
)
async def show_all_members(
    message: Message,
    user_service: UserService,
) -> None:

    members = await user_service.user_repository.get_all()

    if not members:
        await message.reply("В клане нет участников")
        return None

    answer = "Список участников клана: \n\n"

    for index, member in enumerate(members, start=1):
        member_dto = UserDTO.from_model(member)
        answer += (
            f"{index}. {user_service.get_full_name(member_dto)} - {member.nickname}\n"
        )

    await message.answer(text=answer)

    return None
