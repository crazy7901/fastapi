from app.crud.crud_user import user_dao
from common.exception import errors
from database.db_mysql import async_db_session
from schemas.user import CreateUserParam
from db.models import User


class UserService:

    @staticmethod  # 用户注册
    async def create_user(user: CreateUserParam):
        async with async_db_session.begin() as db:
            if not user.password:
                raise errors.ForbiddenError(msg="Password is required")
            username = await user_dao.get_(db=db, name=user.username)
            if username:
                raise errors.ForbiddenError(msg="Username already exists")
            await user_dao.create(db, obj=user)
        return user

    @staticmethod
    async def get_user(self, user_id):
        async with async_db_session.begin() as db:
            pass

user_service = UserService()