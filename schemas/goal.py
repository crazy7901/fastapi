from pydantic import BaseModel


class BaseGoalParm(BaseModel):
    raceId: int | None = None
    userId: int | None = None
    eventId: int | None = None
    goalTime: str | None = None
    goalType: str | None = None
    club: str | None = None
    scoredClub: str | None = None
