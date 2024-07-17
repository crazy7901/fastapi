from fastapi import APIRouter
from app.api.race.api_race import router as race_router

router = APIRouter(prefix="/race", tags=["比赛部分"])

router.include_router(race_router)