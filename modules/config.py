from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    PRODUCTION: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

