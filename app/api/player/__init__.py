from fastapi import APIRouter
from app.api.player.api_player import router as player_router

router = APIRouter(prefix="/player", tags=["球员部分"])

router.include_router(player_router)