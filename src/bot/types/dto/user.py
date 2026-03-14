from pydantic import BaseModel

from ...models import User


class UserDTO(BaseModel):
    """ДТО класс для хранения пользователя aiogram без зависимости от библиотеки"""

    id: int
    first_name: str
    nickname: str | None = None
    last_name: str | None = None
    username: str | None = None

    # Другие поля появятся по мере обновлений и добавления базы данных

    def to_model(self) -> User:
        """Преобразует DTO в модель SQLAlchemy User

        Returns:
            User: экземпляр модели User для сохранения в БД
        """

        return User(
            telegram_id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            nickname=self.nickname,
        )

    @classmethod
    def from_model(cls, user: User) -> "UserDTO":
        """Создает DTO из модели SQLAlchemy User

        Args:
            user: User - модель пользователя из БД

        Returns:
            UserDTO: DTO объект пользователя
        """

        return cls(
            id=user.telegram_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            nickname=user.nickname,
        )


__all__ = [
    "UserDTO",
]
