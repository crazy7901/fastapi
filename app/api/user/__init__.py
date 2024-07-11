from fastapi import APIRouter
from app.api.user.api_user import router as user_router

router = APIRouter(prefix="/user", tags=["用户部分"])

router.include_router(user_router)