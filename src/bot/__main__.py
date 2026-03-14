import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config import settings
from .database import create_tables
from .middlewares import DatabaseMiddleware
from .routers import include_routers

logging.basicConfig(level=logging.DEBUG)


async def main():
    await create_tables()

    bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    dp.update.middleware(DatabaseMiddleware())
    include_routers(dp)

    await dp.start_polling(bot)


asyncio.run(main())
