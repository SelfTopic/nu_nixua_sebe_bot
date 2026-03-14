import logging
import re
from typing import Any

from aiogram.filters import Filter
from aiogram.types import Message

logger = logging.getLogger(__name__)


class Text(Filter):
    """Кастомный универсальный фильтр для текста.

    Example:
        @router.message(Text(command="привет"))
        async def hello_handler(message: Message):
            text = message.text # привет


    """

    def __init__(
        self,
        lower: bool = True,
        command: str | None = None,
        startswith: str | None = None,
        pattern: str | None = None,
    ) -> None:
        self.lower = lower
        self.command = command
        self.startswith = startswith
        self.pattern = pattern

    async def __call__(self, message: Message) -> bool | dict[str, Any]:
        text = message.text

        if not text:
            return False

        if self.lower:
            text = text.lower()

        if (
            self.command and text != self.command.lower()
            if self.lower
            else self.command
        ):
            return False

        if self.startswith:
            start_check = self.startswith.lower() if self.lower else self.startswith
            if not text.startswith(start_check):
                return False

        if self.pattern:
            matches = re.search(self.pattern, text)
            if not matches:
                return False
            if matches.groupdict():
                return matches.groupdict()

        return True
