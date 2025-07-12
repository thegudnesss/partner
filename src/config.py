
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    redis_host: str = "localhost"
    default_language: str = "en"
    mongo_uri: str = 'localhost:27017'
    mongo_db_name: str = "botconfig"
    logs_channel: int | None = None

    class Config:
        env_file = "data/config.env"
        env_file_encoding = "utf-8"


config = Settings()  # type: ignore[arg-type]
