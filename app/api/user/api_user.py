import random
import re
import time

from fastapi import APIRouter, UploadFile, File
from fastapi.params import Depends

from app.crud.crud_player import player_dao
from app.crud.crud_user import user_dao
from common.response.response_schema import response_base, ResponseModel
from db.database import async_db_session
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
async def register(toaddr: str, f: int = 0) -> ResponseModel:  # flag为1意味着注册，不能有重复的
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    flag = bool(re.match(regex, toaddr))
    if not flag:
        return await response_base.fail(data="邮箱格式不正确")
    else:
        if f:
            duplicateFlag = await user_service.getEmail(email=toaddr)
            if duplicateFlag:
                return await response_base.fail(data="该邮箱已被注册")
        # 发送邮件验证码
        captcha = str(random.randint(100000, 999999))
        dict_captcha[toaddr] = captcha
        dict_captcha[toaddr + "time"] = time.time()
        mess = "您的验证码为:" + captcha
        result = await send_email(mess=mess, to_addr=toaddr)
        if result:
            return await response_base.success(data="验证码已发送")
        else:
            return await response_base.fail(data="验证码发送失败")


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
        async with async_db_session.begin() as db:
            await user_dao.update_userinfo(db=db, id=current_user['username'], obj={"clubId": data[1].id})
            await player_dao.update_player(db=db, id=current_user['username'], obj={"clubId": data[1].id, "flag": 1})
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
    userId: int
    decision: int


@router.post("/clubDecide", summary="对申请加入的球员进行处理")
async def clubDecide(playerinfo: PlayerUser, current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await club_service.club_decide(playerinfo=playerinfo, creator=current_user['username'])
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])


@router.get("/avatar", summary="获取用户头像")
async def avatar(current_user: dict = Depends(get_current_token)) -> ResponseModel:
    id = current_user['username']
    object_name = f'player/{id}.png'

    # 生成下载文件的签名URL，有效时间为3600秒。
    # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
    url = bucket.sign_url('GET', object_name, 3600, slash_safe=True)
    return await response_base.success(data=url)


@router.post("/updateAvatar", summary='上传用户头像')
async def upload_image(file: UploadFile = File(...), current_user: dict = Depends(get_current_token)):
    contents = await file.read()
    username = current_user['username']

    bucket.put_object(f'player/{username}.png', contents)
    # 处理图像
    # ...

    return await response_base.success(data="Image processed successfully")


@router.post("/clubAvatar", summary='上传俱乐部头像')
async def upload_image(clubId: str | int, file: UploadFile = File(...)):
    contents = await file.read()
    bucket.put_object(f'club/{str(clubId)}.png', contents)
    # 处理图像
    # ...

    return await response_base.success(data="Image processed successfully")


@router.get("/getImage/{name}", summary="获取小程序所需的图片")
async def logos(name) -> ResponseModel:
    object_name = f'app/{name}.png'

    # 生成下载文件的签名URL，有效时间为3600秒。
    # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
    url = bucket.sign_url('GET', object_name, 3600, slash_safe=True)
    return await response_base.success(data=url)


@router.get("/detail", summary="个人资料卡")
async def detail(current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await user_service.get_detail(id=current_user['username'])
    return await response_base.success(data=data)


@router.get("/Playerdetail", summary="球员卡")
async def PLayerdetail(current_user: dict = Depends(get_current_token)) -> ResponseModel:
    data = await user_service.get_detail(id=current_user['username'])
    return await response_base.success(data=data)
