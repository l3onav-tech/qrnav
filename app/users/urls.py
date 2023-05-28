from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, Security, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from sqlalchemy.sql.functions import current_user

from app.settings.database import get_session
from app.users.models import User, Role, UserToRole
from app.users.schemas import SignUpRequest, SignInRequest
from app.users.auth import AuthHandler

auth_handler = AuthHandler()

router = APIRouter(prefix="/v1/auth")

ACCESS_TOKEN_EXPIRE_MINUTES = 43200

@router.post("/is_authenticated")
async def is_authenticated(
    current_user: str = Depends(auth_handler.auth_wraper),
):
    return { "user": current_user, "message": "You are in" }

@router.post("/signin")
async def login_for_access_token(
    current_user: SignInRequest,
    response: Response,
    api_token: Annotated[str | None, Cookie()] = None,
    session: Session = Depends(get_session),
):
    if api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are already logged in",
        )
    user = session.query(User).filter(User.email == current_user.email).first()
    if (not current_user) or (not auth_handler.verify_password(current_user.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = auth_handler.encode_token(user.email)
    response.set_cookie(
        key="api_token",
        value=access_token,
        httponly=True,
        secure=False,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"message": "Welcome Back!", "user": user.email}

@router.post("/signup")
def sign_up(user: SignUpRequest, session: Session = Depends(get_session)):
    already_exists = user.email in [session.query(User).filter("email" == user.email.lower()).first()]
    # Check if user already exists
    if already_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    hashed_password = auth_handler.get_password_hash(user.password)
    role = session.query(Role).first()
    user_to_role = UserToRole()
    user_to_role.role = role
    new_user = User(email=user.email.lower(), username=user.username, password=hashed_password)
    new_user.roles.append(user_to_role)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    if new_user.id is None:
        raise HTTPException(status_code=500, detail="Error creating user")

    return { "createdwithsuccess": True, "message": "Welcome to the club!" }
