from datetime import datetime

from sqlalchemy import BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    nickname: Mapped[str] = mapped_column()  # Ник в игре
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str | None] = mapped_column()

    username: Mapped[str | None] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


__all__ = [
    "User",
]
