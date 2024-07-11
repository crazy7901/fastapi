from pydantic import BaseModel


class CreateClubParam(BaseModel):
    name: str
    captain: int | None = None
    avatar: int = 0