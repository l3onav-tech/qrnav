from fastapi import APIRouter, Depends, HTTPException, Response, Cookie,status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from app.settings.database import get_session
from app.users.auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from app.users.models import User, Role, UserToRole
from app.users.schemas import UserIn

router = APIRouter(prefix="/v1/auth")

ACCESS_TOKEN_EXPIRE_MINUTES = 43200

@router.post("/is_authenticated")
def is_authenticated(api_token: Annotated[str | None, Cookie()] = None ):
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are already logged in",
        )
    user = get_current_user(api_token)
    if user:
        raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are already logged in",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value= access_token, httponly=True)
    return { "user": user.email, "message": "You are in" }

@router.post("/signin")
async def login_for_access_token(
    user: UserIn,
    response: Response,
    api_token: Annotated[str | None, Cookie()] = None,
):
    if api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are already logged in",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    user = authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    print("access_token: ", access_token)
    response.set_cookie(
        key="api_token",
        value=access_token,
        httponly=True,
        secure=False,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"message": "Welcome Back!", "user": user.email}

@router.post("/signup")
def sign_up(user: UserIn, session: Session = Depends(get_session)):
    already_exists = user.email in [session.query(User).filter("email" == user.email).first()]
    # Check if user already exists
    if already_exists:
        # TODO: Return a better error message
        raise HTTPException(status_code=400, detail="Email already registered")

    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = get_password_hash(user.password)
    role = session.query(Role).first()
    user_to_role = UserToRole()
    user_to_role.role = role
    new_user = User(email=user.email, username=user.username, password=hashed_password)
    new_user.roles.append(user_to_role)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    if new_user.id is None:
        raise HTTPException(status_code=500, detail="Error creating user")

    return { "createdwithsuccess": True, "message": "Welcome to the club!" }
