from typing import Type

from sqlalchemy import and_, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from core.crud import ModelType
from db.models import Club
from schemas.club import (
    CreateClubParam
)


# from common.msd.crud import CRUDBase
# from common.security.jwt import get_hash_password
# from utils.timezone import timezone


# class CRUDUser(CRUDBase[User, CreateUserParam,UpdateUserParam]):
class CRUDUser:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_club(self, db: AsyncSession, id: str | int = None, name: str | None = None):
        if name is not None:
            clubs = await db.execute(select(self.model).where(self.model.name == name))
            return clubs.scalars().all()
        if id is not None:
            clubs = await db.execute(select(self.model).where(self.model.id == id))
            return clubs.scalars().all()

    async def create_club(self, db: AsyncSession, obj: CreateClubParam):
        dict_obj = obj.model_dump()
        #     dict_obj.update({'salt': None})
        new_club = self.model(**dict_obj)
        db.add(new_club)


club_dao: CRUDUser = CRUDUser(Club)
