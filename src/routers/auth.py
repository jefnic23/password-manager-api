from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.dependencies import AUTH_SERVICE_DEPENDENCY
from src.schemas.token import Token
from src.schemas.token_refresh_request import TokenRefreshRequest

router = APIRouter()


@router.post("/login")
async def login(
    auth_service: AUTH_SERVICE_DEPENDENCY,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await auth_service.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.generate_access_token(sub=user.id)
    refresh_token = await auth_service.generate_refresh_token(sub=user.id)
    return Token(
        access_token=access_token, token_type="bearer", refresh_token=refresh_token
    )


@router.post("/refresh")
async def refresh_access(
    auth_service: AUTH_SERVICE_DEPENDENCY,
    body: TokenRefreshRequest,
) -> Token:
    payload = auth_service.verify_token(body.refresh_token)
    user_id: int | None = int(payload.get("sub"))
    access_token = auth_service.generate_access_token(sub=user_id)
    refresh_token = await auth_service.generate_refresh_token(sub=user_id)
    return Token(
        access_token=access_token, token_type="bearer", refresh_token=refresh_token
    )
