import datetime

from pydantic import BaseModel


class BaseMatchPlayerParam(BaseModel):
    userId: int



class CreateMatchPlayerParam(BaseMatchPlayerParam):
    name: str | None = None
    position: str | None = None
    number: int | None = None
    club: str | None = None
    raceId: int | None = None
    # goalsScoredInFriendlies: int = 0
    # goalsScoredInChallenges: int = 0
    # createdTime: datetime.datetime = datetime.datetime.now()


class UpdateMatchPlayerParam(BaseMatchPlayerParam):
    # email: str
    name: str | None = None
    club: str | None = None
    position: str | None = None
    number: int | None = None
    flag: int | None = None
