from pydantic import BaseModel


class BaseUserParm(BaseModel):
    name: str
    password: str


class CreateUserParam(BaseUserParm):
    email: str
    role: int = 1000


class UpdateUserParam(BaseUserParm):
    # email: str
    role: int | None = None
    password: str | None = None
    name: str | None = None
    email: str | None = None
    # avatar: int | None = None
