from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated, Optional


from app.settings.database import get_session
from app.users.models import User, Role, UserToRole
from app.users.schemas import SignUpRequest, SignInRequest 
from app.users.auth import authenticate_user, create_access_token, get_current_active_user


router = APIRouter(prefix="/v1/auth")

ACCESS_TOKEN_EXPIRE_MINUTES = 43200

@router.post("/is_authenticated")
async def is_authenticated(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    return { "user": current_user, "message": "You are in" }

@router.post("/signin")
async def login_for_access_token(
    form_data: SignInRequest,
):
    if  (
        not form_data.username 
        and not form_data.email 
    ) or (
        not form_data.password 
    ) or (
        not authenticate_user( username=form_data.username, password=form_data.password )
        and not authenticate_user( username=form_data.email, password=form_data.password )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": form_data.email.lower(), "scopes": ["me"]})
    return {
        "message": "Welcome Back!",
        "user": form_data.email.lower(),
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.post("/signup")
def sign_up(user: SignUpRequest, session: Session = Depends(get_session)):
    already_exists = user.email in [session.query(User).filter("email" == user.email.lower()).first()]
    # Check if user already exists
    if already_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    hashed_password =get_password_hash(user.password)
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
