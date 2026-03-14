from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from ...callback import ClanRequestCallback
from ...filters import OwnerFilter, UserFilter
from ...services import UserService
from ...storage.clan_requests import pending_requests
from ...types import UserDTO

router = Router(name=__name__)


@router.callback_query(
    ClanRequestCallback.filter(F.action == "accept"),
    UserFilter(),
    OwnerFilter(),
)
async def accept_request(
    callback: CallbackQuery,
    callback_data: ClanRequestCallback,
    user_service: UserService,
    user: UserDTO,
    bot: Bot,
) -> None:

    user_dto = pending_requests.get(callback_data.telegram_id)
    if not user_dto:
        await callback.answer(
            "Заявка для этого пользователя устарела или уже обработана", show_alert=True
        )
        return None

    existing = await user_service.user_repository.get(by=user_dto)
    if existing:
        await callback.answer("Этот игрок уже в клане", show_alert=True)
        return None

    await user_service.user_repository.insert(insert_data=user_dto)
    pending_requests.pop(callback_data.telegram_id)

    await bot.send_message(
        chat_id=callback_data.telegram_id,
        text=f"Ты принят в клан под ником {user_dto.nickname} ✅",
    )

    assert isinstance(callback.message, Message)
    assert callback.message.text

    await callback.message.edit_text(
        text=callback.message.text + "\n\n✅ Принят",
        reply_markup=None,
    )
    await callback.answer()


@router.callback_query(
    ClanRequestCallback.filter(F.action == "reject"),
    OwnerFilter(),
)
async def reject_request(
    callback: CallbackQuery,
    callback_data: ClanRequestCallback,
    bot: Bot,
) -> None:
    await bot.send_message(
        chat_id=callback_data.telegram_id,
        text="Твоя заявка на вступление отклонена ❌",
    )

    assert isinstance(callback.message, Message)
    assert callback.message.text

    pending_requests.pop(callback_data.telegram_id, None)

    await callback.message.edit_text(
        text=callback.message.text + "\n\n❌ Отклонён",
        reply_markup=None,
    )
    await callback.answer()
