import base64
import random
import re
import time
from typing import List

from fastapi import APIRouter, UploadFile, File
from fastapi.params import Depends

from common.response.response_schema import response_base, ResponseModel
from schemas.club import CreateClubParam
from schemas.user import *
from service.club_service import club_service
from service.user_service import user_service
from util.email import send_email, dict_captcha
from util.token import get_current_token

router = APIRouter()
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称，例如examplebucket。
bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'victory-greens')


# 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@router.post("/sendEmail/{toaddr}", summary="发送邮件验证码")
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


@router.post("/register/{captcha}", summary="注册接口")
async def register(user: CreateUserParam, captcha) -> ResponseModel:
    data = await user_service.create_user(user=user, captcha=captcha)
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])


@router.post("/login", summary="账号登录接口")
async def login(user: BaseUserParm) -> ResponseModel:
    data = await user_service.check_user(user)
    data = {
        "token": data,
        "username": user.name
    }
    if data["token"]:
        return await response_base.success(data=data)
    else:
        return await response_base.fail(data="用户名或密码错误")


@router.post("/emaillogin/{captcha}", summary="邮箱登录接口")
async def emaillogin(user: UpdateUserParam, captcha) -> ResponseModel:
    email = user.email
    data = await user_service.check_email(email=email, captcha=captcha)
    if data[0]:
        return await response_base.success(data={"token": data[1], "username": data[2]})
    else:
        return await response_base.fail(data=data[1])


@router.post("/createClub", summary="创建俱乐部")
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


@router.put("/reset/{captcha}", summary="重置密码接口")
async def reset(user: UpdateUserParam, captcha) -> ResponseModel:
    data = await user_service.update_password(captcha=captcha, update_user=user)
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])


@router.put("/update", summary="修改用户信息")
async def update(user: UpdateUserParam, current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await user_service.update_user(update_user=user, username=current_user['username'])
    if data:
        return await response_base.success(data="修改成功")
    else:
        return await response_base.fail(data="修改失败")


# @router.get("/avatar", summary="获取头像集")
# async def avatar_list() -> ResponseModel:
#     avatars = {}
#     for i in range(0, 12):
#         with open('./img/' + str(i) + '.png', 'rb') as f:
#             image_base64 = base64.b64encode(f.read())
#             avatars[i] = image_base64
#         # avatars[i]='1'
#     return await response_base.success(data=avatars)


# @router.put("/updateAvatar", summary="更新头像")
# async def update_avatar(user: UpdateUserParam, current_user: dict = Depends(get_current_token)) -> ResponseModel:
#     data = await user_service.update_user(update_user=user, username=current_user['username'])
#     if data:
#         return await response_base.success(data="修改成功")
#     else:
#         return await response_base.fail(data="修改失败")


@router.get("/getApplication", summary="获取申请列表")
async def getApplication(current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await user_service.getApplication(username=current_user['username'])
    return await response_base.success(data=data)


class PlayerUser(BaseModel):
    userId: str
    decision: int


@router.post("/clubDecide", summary="对申请加入的球员进行处理")
async def clubDecide(playerinfo: PlayerUser, current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await club_service.club_decide(playerinfo=playerinfo, creator=current_user['username'])
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])


@router.get("/avatar", summary="获取用户头像")
async def avatar(user: UpdateUserParam) -> ResponseModel:
    username = user.name
    object_name = f'player/{username}.png'

    # 生成下载文件的签名URL，有效时间为3600秒。
    # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
    url = bucket.sign_url('GET', object_name, 3600, slash_safe=True)
    return await response_base.success(data=url)


@router.post("/updateAvatar")
async def upload_image(file: UploadFile = File(...), current_user: dict = Depends(get_current_token)):
    contents = await file.read()
    username = current_user['username']
    bucket.put_object(f'player/{username}.png', contents)
    # 处理图像
    # ...

    return await response_base.success(data="Image processed successfully")
