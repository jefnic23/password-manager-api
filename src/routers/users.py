from fastapi import APIRouter

from src.dependencies import CURRENT_USER_DEPENDENCY

router = APIRouter()


@router.get("/users")
async def get_user(current_user: CURRENT_USER_DEPENDENCY) -> str:
    return current_user.email
