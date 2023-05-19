from typing import Optional
from requests import options
from pydantic import BaseModel, Field


class TapSchema(BaseModel):
    name: str = Field(min_length=2, max_length=256)
    note: str = Field(min_length=2, max_length=1024)
