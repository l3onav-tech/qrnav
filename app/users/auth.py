from typing import Annotated, Optional
from fastapi import Depends, HTTPException, Security, Cookie,status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from jose import jwt
from passlib.context import CryptContext

from app.settings import get_settings
from app.settings.database import engine
from app.users.models import User

class AuthHandler:

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = get_settings().SECRET_KEY
    algorithm = "HS256"

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, email: str):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "sub": email,
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Signature has expired",
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    def auth_wraper(self, api_token: Annotated[str | None, Cookie()] = None):
        return self.decode_token(api_token)
