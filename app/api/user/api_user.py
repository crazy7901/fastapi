import base64
import random
import re
import time

from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from common.response.response_schema import response_base, ResponseModel
from schemas.club import CreateClubParam
from schemas.user import *
from service.club_service import club_service
from service.user_service import user_service
from util.token import get_current_token
from util.email import send_email, dict_captcha

router = APIRouter()


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@router.post("/sendEmail/{toaddr}", description="发送邮件验证码")
async def register(toaddr: str) -> ResponseModel:
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    flag = bool(re.match(regex, toaddr))
    if not flag:
        return await response_base.fail(data="邮箱格式不正确")
    else:
        # 发送邮件验证码
        captcha = str(random.randint(100000, 999999))
        dict_captcha[toaddr] = captcha
        dict_captcha[toaddr + "time"] = time.time()
        mess = "您的验证码为:" + captcha
        await send_email(mess=mess, to_addr=toaddr)
        return await response_base.success(data="验证码已发送")


@router.post("/register/{captcha}", description="注册接口")
async def register(user: CreateUserParam, captcha) -> ResponseModel:
    data = await user_service.create_user(user=user, captcha=captcha)
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])


@router.post("/login", description="登录接口")
async def login(user: BaseUserParm) -> ResponseModel:
    data = await user_service.check_user(user)
    if data:
        return await response_base.success(data=data)
    else:
        return await response_base.fail(data="用户名或密码错误")


@router.post("/createClub", description="创建俱乐部")
async def createClub(club: CreateClubParam, current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await club_service.create_club(club, creator=current_user['username'])
    if data[0]:
        club_detail = {
            "name": data[1].name,
            "id": data[1].id,
            "captain": data[1].captain
        }
        return await response_base.success(data=club_detail)
    else:
        return await response_base.fail(data=data[1])


@router.put("/reset/{captcha}", description="重置密码接口")
async def reset(user: UpdateUserParam, captcha) -> ResponseModel:
    data = await user_service.update_password(captcha=captcha, update_user=user)
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])


@router.put("/update", description="修改用户信息")
async def update(user: UpdateUserParam, current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await user_service.update_user(update_user=user, username=current_user['username'])
    if data:
        return await response_base.success(data="修改成功")
    else:
        return await response_base.fail(data="修改失败")


@router.get("/avatar", description="获取头像集")
async def avatar_list() -> ResponseModel:
    avatars = {}
    for i in range(0, 12):
        with open('./img/' + str(i) + '.png', 'rb') as f:
            image_base64 = base64.b64encode(f.read())
            avatars[i] = image_base64
        # avatars[i]='1'
    return await response_base.success(data=avatars)


@router.put("/updateAvatar", description="更新头像")
async def update_avatar(user: UpdateUserParam, current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await user_service.update_user(update_user=user, username=current_user['username'])
    if data:
        return await response_base.success(data="修改成功")
    else:
        return await response_base.fail(data="修改失败")
