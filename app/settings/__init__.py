from .settings import *
from .settings import Settings
from .redis import *
from functools import lru_cache


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
