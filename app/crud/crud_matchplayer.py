from typing import Type

from sqlalchemy import select, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import ModelType
from db.models import MatchPlayers
from schemas.matchplayer import CreateMatchPlayerParam


class CRUDPlayer:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_matchplayer(self, db: AsyncSession, club: str | None = None, name: str | None = None,
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

    async def create_matchplayer(self, db: AsyncSession, obj: CreateMatchPlayerParam) -> None:
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

    async def update_matchplayer(self, db: AsyncSession, id, obj: dict):
        """
        更新用户信息

        :param db:
        :param input_user:
        """
        user = await db.execute(update(self.model).where(self.model.userId == id).values(obj))
        return user.rowcount

    async def delete(self, db: AsyncSession, user_id: int | None = None, club: str | None = None,
                     raceId: int | None = None) -> int:
        """
        删除用户

        :param db:
        :param user_id:
        :return:
        """
        if user_id is not None:
            user = await db.execute(delete(self.model).where(self.model.userId == user_id))
        if club is not None:
            user = await db.execute(delete(self.model).where(and_(*[self.model.club == club, self.model.raceId == raceId])))
        return user.rowcount


matchplayer_dao: CRUDPlayer = CRUDPlayer(MatchPlayers)
