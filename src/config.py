from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "REST API"
    VERSION: str = "0.1.0"

    DEBUG: bool = True

    ROOT_PATH: str = "/src/"
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
    TCP_PORT: int = 8000

    POSTGRES_HOST: str = ""
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
