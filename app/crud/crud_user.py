#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Type

from sqlalchemy import and_, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from core.crud import ModelType
from db.models import User
from schemas.user import (
    CreateUserParam, UpdateUserParam
)


# from common.msd.crud import CRUDBase
# from common.security.jwt import get_hash_password
# from utils.timezone import timezone


# class CRUDUser(CRUDBase[User, CreateUserParam,UpdateUserParam]):
class CRUDUser:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: str | None = None, name: str | None = None):
        """
        获取用户

        :param name:
        :param db:
        :param id:
        :return:
        """
        if name is not None:
            users = await db.execute(select(self.model).where(self.model.name == name))
            return users.scalars().all()
        if id is not None:
            users = await db.execute(select(self.model).where(self.model.id == id))
            return users.scalars().all()

    async def create(self, db: AsyncSession, obj: CreateUserParam, *, social: bool = False) -> None:
        """
        创建用户

        :param db:
        :param obj:
        :param social:
        :return:
        """
        dict_obj = obj.model_dump()
        #     dict_obj.update({'salt': None})
        new_user = self.model(**dict_obj)
        db.add(new_user)

    async def update_userinfo(self, db: AsyncSession, input_user: User, obj: dict) -> int:
        """
        更新用户信息

        :param db:
        :param input_user:
        :param obj:
        :return:
        """
        user = await db.execute(update(self.model).where(self.model.id == input_user.id).values(obj))
        return user.rowcount

    # async def update_avatar(self, db: AsyncSession, current_user: User, avatar: AvatarParam) -> int:
    #     """
    #     更新用户头像
    #
    #     :param db:
    #     :param current_user:
    #     :param avatar:
    #     :return:
    #     """
    #     user = await db.execute(update(self.model).where(self.model.id == current_user.id).values(avatar=avatar.url))
    #     return user.rowcount

    async def delete(self, db: AsyncSession, user_id: int) -> int:
        """
        删除用户

        :param db:
        :param user_id:
        :return:
        """
        return await self.delete_(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> User | None:
        """
        检查邮箱是否存在

        :param db:
        :param email:
        :return:
        """
        mail = await db.execute(select(self.model).where(self.model.email == email))
        return mail.scalars().first()

    async def reset_password(self, db: AsyncSession, pk: int, password: str, salt: str) -> int:
        """
        重置用户密码

        :param db:
        :param pk:
        :param password:
        :param salt:
        :return:
        """
        user = await db.execute(
            update(self.model).where(self.model.id == pk).values(password=password)
        )
        return user.rowcount

    async def get_list(self, dept: int = None, username: str = None, phone: str = None, status: int = None) -> Select:
        """
        获取用户列表

        :param dept:
        :param username:
        :param phone:
        :param status:
        :return:
        """
        se = (
            select(self.model)
            .options(selectinload(self.model.dept))

            # .options(selectinload(self.model.roles).selectinload(Role.menus))

            .order_by(desc(self.model.join_time))
        )
        where_list = []
        if dept:
            where_list.append(self.model.dept_id == dept)
        if username:
            where_list.append(self.model.username.like(f'%{username}%'))
        if phone:
            where_list.append(self.model.phone.like(f'%{phone}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        return se
    # async def update_login_time(self, db: AsyncSession, username: str) -> int:
    #     """
    #     更新用户登录时间
    #
    #     :param db:
    #     :param username:
    #     :return:
    #     """
    #     user = await db.execute(
    #         update(self.model).where(self.model.username == username).values(last_login_time=timezone.now())
    #     )
    #     return user.rowcount
    # async def get_super(self, db: AsyncSession, user_id: int) -> bool:
    #     """
    #     获取用户超级管理员状态
    #
    #     :param db:
    #     :param user_id:
    #     :return:
    #     """
    #     user = await self.get(db, user_id)
    #     return user.is_superuser

    # async def get_staff(self, db: AsyncSession, user_id: int) -> bool:
    #     """
    #     获取用户后台登录状态
    #
    #     :param db:
    #     :param user_id:
    #     :return:
    #     """
    #     user = await self.get(db, user_id)
    #     return user.is_staff
    #
    # async def get_status(self, db: AsyncSession, user_id: int) -> bool:
    #     """
    #     获取用户状态
    #
    #     :param db:
    #     :param user_id:
    #     :return:
    #     """
    #     user = await self.get(db, user_id)
    #     return user.status
    #
    # async def get_multi_login(self, db: AsyncSession, user_id: int) -> bool:
    #     """
    #     获取用户多点登录状态
    #
    #     :param db:
    #     :param user_id:
    #     :return:
    #     """
    #     user = await self.get(db, user_id)
    #     return user.is_multi_login
    #
    # async def set_super(self, db: AsyncSession, user_id: int) -> int:
    #     """
    #     设置用户超级管理员
    #
    #     :param db:
    #     :param user_id:
    #     :return:
    #     """
    #     super_status = await self.get_super(db, user_id)
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == user_id).values(is_superuser=False if super_status else True)
    #     )
    #     return user.rowcount
    #
    # async def set_staff(self, db: AsyncSession, user_id: int) -> int:
    #     """
    #     设置用户后台登录
    #
    #     :param db:
    #     :param user_id:
    #     :return:
    #     """
    #     staff_status = await self.get_staff(db, user_id)
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == user_id).values(is_staff=False if staff_status else True)
    #     )
    #     return user.rowcount
    #
    # async def set_status(self, db: AsyncSession, user_id: int) -> int:
    #     """
    #     设置用户状态
    #
    #     :param db:
    #     :param user_id:
    #     :return:
    #     """
    #     status = await self.get_status(db, user_id)
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == user_id).values(status=False if status else True)
    #     )
    #     return user.rowcount
    #
    # async def set_multi_login(self, db: AsyncSession, user_id: int) -> int:
    #     """
    #     设置用户多点登录
    #
    #     :param db:
    #     :param user_id:
    #     :return:
    #     """
    #     multi_login = await self.get_multi_login(db, user_id)
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == user_id).values(is_multi_login=False if multi_login else True)
    #     )
    #     return user.rowcount
    #
    # async def get_with_relation(self, db: AsyncSession, *, user_id: int = None, username: str = None) -> User | None:
    #     """
    #     获取用户和（部门，角色，菜单）
    #
    #     :param db:
    #     :param user_id:
    #     :param username:
    #     :return:
    #     """
    #     where = []
    #     if user_id:
    #         where.append(self.model.id == user_id)
    #     if username:
    #         where.append(self.model.username == username)
    #     user = await db.execute(
    #         select(self.model)
    #         .options(selectinload(self.model.dept))
    #         # .options(selectinload(self.model.roles).joinedload(Role.menus))
    #         .where(*where)
    #     )
    #     return user.scalars().first()


user_dao: CRUDUser = CRUDUser(User)
