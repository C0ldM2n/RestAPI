import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = 'REST API'
    BASE_DIR: str = str(os.path.dirname(os.path.abspath(__file__)))
    # SECRET_KEY: str
    TCP_PORT: int = 8000
    VERSION: str = '0.1.0'
    DEBUG: bool = True
    ROOT_PATH: str = '/src/'
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, '.env'), env_file_encoding='utf-8')

    @property
    def db_url(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = Settings()
