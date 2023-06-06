from typing import Annotated, Optional
from botocore.utils import email
from fastapi import Depends, HTTPException, Security, Cookie,status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from pydantic import ValidationError
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.settings import get_settings
from app.settings.database import get_session, engine
from app.users.models import User
from app.users.schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/v1/auth/signin",
    scopes={"me": "Read information about the current user."},
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = get_settings().SECRET_KEY
expires_delta = get_settings().access_token_expire_minutes
algorithm = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    with Session(engine) as session:
        user = session.query(User).filter(User.email == username).first()
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=get_settings().access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt 

async def get_current_user(
    security_scopes: SecurityScopes,
    api_token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(api_token, SECRET_KEY, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, email=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = session.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
    
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])]
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
