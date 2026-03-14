from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr = Field(default=...)
    DATABASE_URL: str = Field(default=...)
    OWNER_TELEGRAM_ID: int = Field(default=...)
    CLAN_CHAT_ID: int = Field(default=...)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
