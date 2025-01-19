from urllib.parse import quote

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, extra="ignore", env_prefix="IMAGES_SERVICE__")
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @computed_field
    @property
    def DATABASE_URI(self) -> str:
        return f"postgresql+asyncpg://{quote(self.POSTGRES_USER)}:{quote(self.POSTGRES_PASSWORD)}@{quote(self.POSTGRES_HOST)}:{self.POSTGRES_PORT}/{quote(self.POSTGRES_DB)}"


settings = Settings()  # type: ignore
