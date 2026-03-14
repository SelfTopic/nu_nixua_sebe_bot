from aiogram.filters.callback_data import CallbackData


class ClanRequestCallback(CallbackData, prefix="clan_request"):
    action: str
    telegram_id: int


__all__ = ["ClanRequestCallback"]
