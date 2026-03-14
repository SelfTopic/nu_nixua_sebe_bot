import logging
from random import choice

from aiogram import Router
from aiogram.types import Message

from ...filters import Text

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(Text(command="бот"))
async def bot_handler(message: Message) -> None:
    logger.debug("Start handling бот command")

    def build_answer() -> str:
        sample = "нихуя себе"

        prefixes = ["ну ", "вот это ", "ахуеть, ", "ну блядь, ", ""]
        postfixes = [", блядь", ", нахуй", ", ебаный в рот", ""]

        return choice(prefixes) + sample + choice(postfixes)

    answer = build_answer()
    logger.debug(f"Generated answer: {answer}")
    await message.reply(text=answer)

    logger.debug("End handling бот command")
    return None
