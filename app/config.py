from pydantic_settings import BaseSettings
import os

# class Settings(BaseSettings):
#     database_hostname: str = "localhost"
#     database_password: str= "johnajohna"
#     database_port: str= "5432"
#     database_username: str= "postgres"
#     database_name: str= "fastapi"
#     secret_key: str= "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#     algorithm: str= "HS256"
#     access_token_expire_minutes: int= 30

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