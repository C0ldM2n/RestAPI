from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy import URL


class Settings(BaseSettings):
    APP_NAME: str = 'REST API'
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
    TCP_PORT: int = 8000
    VERSION: str = '0.1.0'
    DEBUG: bool = 1
    ROOT_PATH: str = '/src/'
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow')

    @property
    def db_url(self) -> [str, URL]:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = Settings()
