from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname: str = os.environ.get("DATABASE_HOSTNAME")
    database_password: str = os.environ.get("DATABASE_PASSWORD")
    database_port: str = os.environ.get("DATABASE_PORT")
    database_username: str = os.environ.get("DATABASE_USERNAME")
    database_name: str = os.environ.get("DATABASE_NAME")
    secret_key: str = os.environ.get("SECRET_KEY")
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

settings = Settings()
