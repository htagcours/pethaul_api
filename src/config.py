# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    ENV_NAME: str = ""
    AWS_REGION_NAME: str = ""
    AWS_PROFILE: str = "" # Pas besoin de le renseigner
    MISTRAL_API_KEY: str = ""
    DYNAMO_TABLE: str = "" # "pethaul-lambda-johndoe24"

    model_config = SettingsConfigDict(env_file=".environ")


settings = Settings()


@lru_cache
def get_settings():
    return settings


env_vars = get_settings()
