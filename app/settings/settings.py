from pydantic import BaseSettings, PostgresDsn
import os


class Settings(BaseSettings):
    app_name: str = "fastapi-skeleton"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    enviroment: str = os.getenv("ENVIRONMENT", "development")
    access_token_expire_minutes: int = 30
    database_url: PostgresDsn = "postgresql://debug:debug@postgres/db"
    OBJECT_STORAGE_ACCESS_KEY: str = os.getenv("OBJECT_STORAGE_ACCESS_KEY")
    OBJECT_STORAGE_SECRET_KEY: str = os.getenv("OBJECT_STORAGE_SECRET_KEY")
    OBJECT_STORAGE_ENDPOINT_PUBLIC: str = os.getenv("OBJECT_STORAGE_ENDPOINT_PUBLIC")
    OBJECT_STORAGE_ENDPOINT_PRIVATE: str = os.getenv("OBJECT_STORAGE_ENDPOINT_PRIVATE")
    OBJECT_STORAGE_REGION: str = os.getenv("OBJECT_STORAGE_REGION")
    GOOGLE_ID_CLIENT: str = os.getenv("GOOGLE_ID_CLIENT")
    GOOGLE_SECRET_CLIENT: str = os.getenv("GOOGLE_SECRET_CLIENT")

    class Config:
        env_file = ".envs"
        env_file_encoding = "utf-8"
