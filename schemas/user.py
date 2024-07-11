from pydantic import BaseModel


class BaseUserParm(BaseModel):
    name: str
    password: str


class CreateUserParam(BaseUserParm):
    email: str | None = None
    role: int = 1000


class UpdateUserParam(BaseUserParm):
    email: str
