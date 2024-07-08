from fastapi import APIRouter

from app.api.router import v1_router

route = APIRouter(prefix="/api")
route.include_router(v1_router)
