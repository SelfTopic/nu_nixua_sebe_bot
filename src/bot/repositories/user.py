import logging

from sqlalchemy import select

from ..exceptions import UserNotFoundError
from ..models import User
from ..types import UserDTO
from .base import Repository

logger = logging.getLogger(__name__)


class UserRepository(Repository):
    """Класс репозиторий для управления сущностью User в базе данных"""

    async def get(
        self,
        by: int | str | UserDTO,
    ) -> User | None:
        """Метод для поиска сущности в базе данных

        Args:
            by: int | str | UserDTO # int для telegram_id, str для username


        Returns:
            User если запись найдена в базе, иначе None
        """

        search_column = User.telegram_id
        search_parameter = by

        if isinstance(by, str):
            search_column = User.username

        elif isinstance(by, UserDTO):
            search_parameter = by.id

        stmt = select(User).filter(search_column == search_parameter).limit(1)

        user = await self.session.scalar(stmt)

        return user

    async def get_all(self) -> list[User] | None:
        """Метод для поиска всех сущностей в базе данных.

        Returns:
            list[User] если записи в базе данных есть, None, если нет"""

        logger.debug("call get_all")

        try:
            users = await self.session.scalars(select(User))
            logger.debug("succsessful getting all users")
            return list(users)

        except Exception as E:
            logger.error(f"Error get all: {E}")
            raise

    async def insert(self, insert_data: UserDTO) -> User:
        """Метод для вставки данных в базу данных

        Args:
            insert_data: UserDTO - Тип с уже готовыми данными для вставки


        Returns:
            User - Модель базы данных с теми же данными

        """
        logger.debug(f"call insert method. insert_data: {insert_data}")

        try:
            user = insert_data.to_model()
            self.session.add(user)
            await self.session.flush()

            logger.debug("Insert data succsessful ")
            return user

        except Exception as E:
            logger.error(f"Error insert data: {E}")
            raise

    async def update(self, update_data: UserDTO):
        """Метод для обновления данных сущности по telegram_id

        Args:
            update_data: UserDTO - класс с уже обновленными данными

        Returns:
            User - модель базы данных с обновленными данными
        """
        logger.debug(f"call update method. update_data: {update_data}")

        try:
            existing_user = await self.get(by=update_data)

            if not existing_user:
                logger.error("Error update data: user not found")
                raise UserNotFoundError("User not found in database")

            existing_user.first_name = update_data.first_name
            existing_user.last_name = update_data.last_name
            existing_user.username = update_data.username

            await self.session.flush()

            logger.debug("Update data succsessful")

            return existing_user

        except Exception as E:
            logger.error(f"Error update data: {E}")
            raise

    async def upsert(self, upsert_data: UserDTO):
        """Метод для вставки или обновления записи. Вставит, если записи нет и обновит, если запись есть

        Args:
            upsert_data: UserDTO - класс с готовыми для вставки/обновления даннными


        Returns:
            User - модель базы данных
        """
        try:
            logger.debug(f"call upsert method. upsert_data: {upsert_data}")

            existing_user = await self.get(by=upsert_data)

            if not existing_user:
                logger.debug("User not found. Calling insert method.")
                return await self.insert(insert_data=upsert_data)

            else:
                logger.debug("User is found. Calling update method.")
                return await self.update(update_data=upsert_data)

        except Exception as E:
            logger.error(f"Error upsert data: {E}")
            raise


__all__ = [
    "UserRepository",
]
