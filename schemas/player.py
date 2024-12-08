import datetime

from pydantic import BaseModel


class BasePlayerParm(BaseModel):
    name: str


class CreatePlayerParam(BasePlayerParm):
    userId: int | None = None
    position: str | None = None
    # goalsScoredInFriendlies: int = 0
    # goalsScoredInChallenges: int = 0
    createdTime: datetime.datetime = datetime.datetime.now()


class UpdatePlayerParam(BasePlayerParm):
    # email: str
    name: str | None = None
    clubId: int | None = None
    position: str | None = None
    number: int | None = None
    flag: int | None = None
