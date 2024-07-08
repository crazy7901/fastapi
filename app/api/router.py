from fastapi import APIRouter

from app.api.user import router as UserRouter

v1_router = APIRouter()
v1_router.include_router(UserRouter)
