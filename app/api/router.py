from fastapi import APIRouter
from app.api.user import router as UserRouter
from app.api.race import router as RaceRouter
from app.api.player import router as PlayerRouter
from app.api.event import router as EventRouter


v1_router = APIRouter()
v1_router.include_router(UserRouter)
v1_router.include_router(RaceRouter)
v1_router.include_router(PlayerRouter)
v1_router.include_router(EventRouter)
