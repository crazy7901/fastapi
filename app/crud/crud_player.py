from typing import Type

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import ModelType
from db.models import Player
from schemas.player import CreatePlayerParam


class CRUDPlayer:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_player(self, db: AsyncSession, club: str | None = None, name: str | None = None,
                         id: int | None = None, number: int | None = None, userId: int | None = None):
        if club is not None:
            players = await db.execute(
                select(self.model).where(self.model.club == club))
            return players.scalars().all()
        if name is not None:
            players = await db.execute(select(self.model).where(self.model.name == name))
            return players.scalars().all()
        if id is not None:
            players = await db.execute(select(self.model).where(self.model.id == id))
            return players.scalars().all()
        if userId is not None:
            players = await db.execute(select(self.model).where(self.model.userId == userId))
            return players.scalars().all()
        if number is not None:
            players = await db.execute(
                select(self.model).where(and_(self.model.startTime == number, self.model.club == club)))
            return players.scalars().all()

    async def create_player(self, db: AsyncSession, obj: CreatePlayerParam) -> None:
        """
        创建用户

        :param db:
        :param obj:
        :return:
        """
        dict_obj = obj.model_dump()
        #     dict_obj.update({'salt': None})
        new_player = self.model(**dict_obj)
        db.add(new_player)

    async def update_player(self, db: AsyncSession, id, obj: dict):
        """
        更新用户信息

        :param db:
        :param input_user:
        """
        user = await db.execute(update(self.model).where(self.model.userId == id).values(obj))
        return user.rowcount


player_dao: CRUDPlayer = CRUDPlayer(Player)
