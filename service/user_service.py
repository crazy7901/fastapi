import time

from schemas.user import *
from service.player_service import player_service
from util.email import dict_captcha
from util.token import *


class UserService:

    @staticmethod  # 用户注册
    async def create_user(user: CreateUserParam, captcha):
        try:
            now = time.time()
            if now - dict_captcha[user.email + "time"] > 300:
                dict_captcha[user.email] = None
                return False, "验证码超时"
            if not dict_captcha[user.email] == captcha:
                return False, "验证码错误"
        except Exception:
            return False, "未发送验证码"
        async with async_db_session.begin() as db:
            if not user.password:
                raise Exception('Password is required')
            username = await user_dao.get(db=db, name=user.name)
            if username:
                print("Username already exists")
                return False, "用户名已存在"
            useremail = await user_dao.get(db=db, email=user.email)
            if useremail:
                print("邮箱已被注册")
                return False, "邮箱已被注册"
            await user_dao.create(db, obj=user)
        dict_captcha[user.email] = None
        return True, user

    @staticmethod  # 查重函数
    async def get_user(id: int | None = None, name: str | None = None):
        async with async_db_session.begin() as db:
            if not id:
                user = await user_dao.get(db=db, id=id)
            if not name:
                user = await user_dao.get(db=db, name=name)
            if id is None and name is None: raise Exception('参数为空')
            return user

    @staticmethod
    async def check_user(obj: BaseUserParm):
        async with async_db_session.begin() as db:
            user = await user_dao.get(db=db, name=obj.name)
            if not user:
                # raise Exception('用户不存在')
                return False
            else:
                if user[0].password == obj.password:
                    token = await generate_access_token(user[0].id)
                    return token
                else:
                    return False

    @staticmethod
    async def check_email(email, captcha):  # 邮箱登录接口
        async with async_db_session.begin() as db:
            user = await user_dao.get(db=db, email=email)
            if not user:
                return False, "用户不存在"
            else:
                try:
                    now = time.time()
                    if now - dict_captcha[email + "time"] > 300:
                        dict_captcha[email] = None
                        return False, "验证码超时"
                    if not dict_captcha[email] == captcha:
                        return False, "验证码错误"
                except Exception:
                    return False, "未发送验证码"
                token = await generate_access_token(user[0].name)
                return True, token, user[0].name

    @staticmethod  # 更新用户密码
    async def update_password(update_user: UpdateUserParam, captcha):
        async with async_db_session.begin() as db:
            user = await user_dao.get(email=update_user.email, db=db)
            try:
                now = time.time()
                user = user[0]
                if now - dict_captcha[user.email + "time"] > 300:
                    dict_captcha[user.email] = None
                    return False, "验证码超时"
                if not dict_captcha[user.email] == captcha:
                    return False, "验证码错误"
            except Exception:
                return False, "未发送验证码"
            dict_captcha[user.email] = None
            id = user.id
            dict = update_user.dict(exclude_unset=True)
            await user_dao.update_userinfo(db, obj=dict, id=id)
            return True, '修改密码成功'

    @staticmethod  # 更新用户所有信息
    async def update_user(username: str | int, update_user: UpdateUserParam):
        async with async_db_session.begin() as db:
            current_user = await user_dao.get(id=username, db=db)
            id = current_user[0].id
            dict = update_user.dict(exclude_unset=True)
            await user_dao.update_userinfo(db, obj=dict, id=id)
            return True

    @staticmethod
    async def getApplication(username: str | int):
        async with async_db_session.begin() as db:
            current_user = await user_dao.get(id=int(username), db=db)
            role = current_user[0].role
            if role // 100 == 11:
                players = await player_service.get_player_by_club(club=current_user[0].club)
                players_dicts = []
                for player in players:
                    dict = {'userId': player.userId, 'name': player.name}
                    if not player.flag:
                        players_dicts.append(dict)
                return players_dicts
            else:
                return False, "您无权申请"

    @staticmethod
    async def getEmail(email: str):
        async with async_db_session.begin() as db:
            user = await user_dao.get(db=db, email=email)
            return user

    @staticmethod
    async def get_detail(email: str | None = None, name: str | None = None, id: int | None = None):
        async with async_db_session.begin() as db:
            if id:
                user = await user_dao.get(db=db, id=id)
            if email:
                user = await user_dao.get(db=db, email=email)
            if name:
                user = await user_dao.get(db=db, name=name)
            return user


user_service = UserService()
