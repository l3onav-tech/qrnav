from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class SignInRequest(BaseModel):
    username: Optional[str] = Field(min_length=2, max_length=16)
    email: Optional[EmailStr]
    password: str = Field(min_length=8, max_length=32)

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    password_confirm: Optional[str] = Field(min_length=8, max_length=32)

class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []

