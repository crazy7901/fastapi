from fastapi import APIRouter, Request
from fastapi.security import OAuth2PasswordBearer
from common.response.response_schema import response_base, ResponseModel
from schemas.user import *
from service.user_service import user_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", description="注册接口")
async def register(user: CreateUserParam) -> ResponseModel:
    data = await user_service.create_user(user=user)
    if data:
        return await response_base.success(data=data)
    else:
        return await response_base.fail(data="注册失败,用户名重复")


@router.post("/login", description="登录接口")
async def login(user: BaseUserParm) -> ResponseModel:
    data = await user_service.check_user(user)
    if data:
        return await response_base.success(data=data)
    else:
        return await response_base.fail(data="用户名或密码错误")
