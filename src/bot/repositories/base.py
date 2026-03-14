from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class Repository(ABC):
    """Базовый класс репозиторий"""

    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        return None


__all__ = ["Repository"]
