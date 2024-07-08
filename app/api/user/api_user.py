from fastapi import APIRouter,Request
from fastapi.security import OAuth2PasswordBearer

from common.response.response_schema import response_base
from schemas.user import CreateUserParam
from service.user_service import user_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/register', description="注册接口")
async def login(user: CreateUserParam):
    await user_service.create_user(user=user)
    return await response_base.success()
