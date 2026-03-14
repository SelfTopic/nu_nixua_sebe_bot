from aiogram import Dispatcher

from .clan.register import router as ClanRegisterRouter
from .clan.show import router as ClanShowRouter
from .common.bot import router as BotRouter
from .common.error import router as ErrorRouter
from .common.start import router as StartRouter
from .owner.request_join import router as OwnerRequestJoinRouter


def include_routers(dp: Dispatcher) -> None:
    """Функция, подключающая все роутеры к основному Дистпетчеру"""

    dp.include_routers(
        StartRouter,
        BotRouter,
        ErrorRouter,
        ClanRegisterRouter,
        ClanShowRouter,
        OwnerRequestJoinRouter,
    )
