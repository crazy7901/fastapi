from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from common.response.response_schema import response_base, ResponseModel
from schemas.club import CreateClubParam
from schemas.user import *
from service.club_service import club_service
from service.user_service import user_service
from test import DependsJwtAuth
from util.token import get_current_token

router = APIRouter()


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@router.post("/createClub", description="创建俱乐部")
async def createClub(club: CreateClubParam, current_user: dict = Depends(get_current_token))->ResponseModel:
    data = await club_service.create_club(club,creator=current_user['username'])
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])

