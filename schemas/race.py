from datetime import datetime

from pydantic import BaseModel


class BaseRaceParm(BaseModel):
    startTime: datetime | None = None
    endTime: datetime | None = None
    homeClub: str | None
    awayClub: str | None = None
    homeTeamJersey: str | None
    awayTeamJersey: str | None = None
    multiPlayer: int | None = None
    venue: int | None = None
    eventId: int | None = None
    homeTeamGoalsScored: int | None = None
    awayTeamGoalsScored: int | None = None


class CreateRaceParam(BaseRaceParm):
    startTime: datetime
    endTime: datetime
    homeClub: str
    awayClub: str
    homeTeamJersey: str
    awayTeamJersey: str
    multiPlayer: int
    venue: int
    eventId: int


class UpdateRaceParam(BaseRaceParm):
    pass
