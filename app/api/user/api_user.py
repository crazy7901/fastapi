from fastapi import APIRouter,Request
from fastapi.security import OAuth2PasswordBearer

from schemas.user import *
from service.user_service import user_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/register', description="注册接口")
async def register(user: CreateUserParam):
    data=await user_service.create_user(user=user)
    return True

@router.post('/login', description="登录接口")
async def login(user: BaseUserParm):
    data=await user_service.