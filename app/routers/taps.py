from fastapi import APIRouter, Depends, HTTPException, Response, Cookie,status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.tap.creation import Tap
from app.tap.schemas import TapSchema
from app.settings.database import get_session
from app.users.auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from app.users.models import User, Role, UserToRole
from app.users.schemas import UserIn, UserRead

router = APIRouter(prefix="/v1/tap")

@router.post("/create")
def create_tap(
    data: TapSchema,
    api_token: Annotated[str | None, Cookie()] = None
):
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not logged in",
        )
    user = get_current_user(api_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not logged in",
        )
    tap = Tap(data, user = str(user.id)).create_tap()
    return {"user": user.email, "tap": tap}

@router.get("{tap_id}")
def read_tap(tap_id: str, api_token: Annotated[str | None, Cookie()] = None):
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not logged in",
        )
    user = get_current_user(api_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not logged in",
        )
    tap = Tap(user = user.id).read_tap(tap_id)
    return tap
