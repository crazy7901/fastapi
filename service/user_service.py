from app.crud.crud_user import user_dao
from db.database import async_db_session
from schemas.user import *
from db.models import User
from util.token import *


class UserService:

    @staticmethod  # 用户注册
    async def create_user(user: CreateUserParam):
        async with async_db_session.begin() as db:
            if not user.password:
                raise Exception('Password is required')
            username = await user_dao.get(db=db, name=user.name)
            if username:
                print("Username already exists")
                return False
            await user_dao.create(db, obj=user)
        return user

    @staticmethod
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
                    token = await generate_access_token(user[0].name)
                    return token
                else:
                    return False


user_service = UserService()
