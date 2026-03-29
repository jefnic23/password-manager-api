from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    SQLALCHEMY_TRACK_MODIFICATIONS: str
    MAIL_SERVER: str
    MAIL_PORT: str
    MAIL_USE_TLS: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()


SETTINGS_DEPENDENCY = Annotated[Settings, Depends(get_settings)]
