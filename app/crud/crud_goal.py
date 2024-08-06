from typing import Type

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import ModelType
from db.models import Goal
from schemas.goal import BaseGoalParm


class CRUDGoal:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_goal(self, db: AsyncSession, club: str | None = None, name: str | None = None,
                         id: int | None = None, number: int | None = None, userId: str | None = None):
        if club is not None:
            goals = await db.execute(
                select(self.model).where(self.model.club == club))
            return goals.scalars().all()
        if name is not None:
            goals = await db.execute(select(self.model).where(self.model.name == name))
            return goals.scalars().all()
        if id is not None:
            goals = await db.execute(select(self.model).where(self.model.id == id))
            return goals.scalars().all()
        if userId is not None:
            goals = await db.execute(select(self.model).where(self.model.userId == userId))
            return goals.scalars().all()
        if number is not None:
            goals = await db.execute(
                select(self.model).where(and_(self.model.startTime == number, self.model.club == club)))
            return goals.scalars().all()

    async def create_goal(self, db: AsyncSession, obj: BaseGoalParm) -> None:
        """
        创建用户

        :param db:
        :param obj:
        :return:
        """
        dict_obj = obj.model_dump()
        #     dict_obj.update({'salt': None})
        new_goal = self.model(**dict_obj)
        db.add(new_goal)

    async def update_goal(self, db: AsyncSession, id, obj: dict):
        """
        更新用户信息

        :param db:
        :param input_user:
        """
        user = await db.execute(update(self.model).where(self.model.userId == id).values(obj))
        return user.rowcount


goal_dao: CRUDGoal = CRUDGoal(Goal)
