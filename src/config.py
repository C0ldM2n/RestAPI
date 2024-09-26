# import os
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from sqlalchemy import URL


class Settings(BaseSettings):
    APP_NAME: str = 'REST API'
    # BASE_DIR: str = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    TCP_PORT: int = 8000
    VERSION: str = '0.1.0'
    DEBUG: bool = 1
    ROOT_PATH: str = '/src/'
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str

    base_dir: ClassVar[Path] = Path(__file__).resolve().parent.parent

    model_config = SettingsConfigDict(
        env_file=str(base_dir / '.env'),
        env_file_encoding='utf-8',
        extra='ignore')

    @property
    def db_url(self) -> [str, URL]:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    # db_url: str = Field(exclude=True)
    #
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.db_url = f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
    #                   f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = Settings()
