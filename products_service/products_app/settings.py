from urllib.parse import quote

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore", env_prefix="PRODUCTS_SERVICE__"
    )
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @computed_field
    @property
    def DATABASE_URI(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}".format(
            user=quote(self.POSTGRES_USER),
            password=quote(self.POSTGRES_PASSWORD),
            host=quote(self.POSTGRES_HOST),
            port=self.POSTGRES_PORT,
            dbname=quote(self.POSTGRES_DB),
        )

settings = Settings()  # type: ignore
