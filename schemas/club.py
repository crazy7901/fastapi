from pydantic import BaseModel


class CreateClubParam(BaseModel):
    name: str
    captain: int
