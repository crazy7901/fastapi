from pydantic import BaseModel


class BaseUserParm(BaseModel):
    name: str
    password: str


class CreateUserParam(BaseUserParm):
    email: str | None = None
    number: int = 0
    role: int = 3


class UpdateUserParam(BaseUserParm):
    email: str
