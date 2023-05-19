from typing import Optional
from requests import options
from pydantic import BaseModel, Field, EmailStr

class SignInRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    user: str
    message: str

class TokenJson(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserIn(BaseModel):
    username: Optional[str] = Field(min_length=2, max_length=32)
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    password_confirm: Optional[str] = Field(min_length=8, max_length=32)

    
class UserRead(BaseModel):
    username: str
    email: str
