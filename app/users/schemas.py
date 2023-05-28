from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    password_confirm: Optional[str] = Field(min_length=8, max_length=32)
