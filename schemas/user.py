from pydantic import BaseModel


class CreateUserParam(BaseModel):
    username: str
    password: str
    email: str
    number: int
    role: int


class UpdateUserParam(BaseModel):
    username: str
    password: str
    email: str
