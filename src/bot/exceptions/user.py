class UserError(Exception):
    """Базовый класс исключение для работы с сущностью User"""

    ...


class UserNotFoundError(UserError):
    """Класс исключение для моментов, когда пользователь не найден"""

    ...
