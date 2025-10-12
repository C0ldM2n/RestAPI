from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    APP_NAME: str = "REST API"
    VERSION: str = "0.4.0"

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    LOG_PATH: Path = Path("./logs/")
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)

    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Config()
