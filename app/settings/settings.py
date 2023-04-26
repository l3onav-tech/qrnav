from pydantic import BaseSettings, PostgresDsn
import os

secretkey = os.getenv("SECRET_KEY", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
env = os.getenv("ENVIROMENT", "development")

class Settings(BaseSettings):
    app_name: str = "qrnav"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    enviroment: str = env
    access_token_expire_minutes: int = 30
    database_url: PostgresDsn = "postgresql://debug:debug@postgres/qrnav"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"




