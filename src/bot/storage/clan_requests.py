from ..types import UserDTO

# { telegram_id: UserDTO }
pending_requests: dict[int, UserDTO] = {}
