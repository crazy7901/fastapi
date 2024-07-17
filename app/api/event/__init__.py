from fastapi import APIRouter
from app.api.event.api_event import router as event_router

router = APIRouter(prefix="/event", tags=["赛事部分"])

router.include_router(event_router)