import datetime
from typing import Type

from sqlalchemy import or_, select, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import ModelType
from db.models import Race
from schemas.race import CreateRaceParam


class CRUDRace:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_race(self, db: AsyncSession, club: str | None = None, now: datetime.datetime | None = None,
                       day: datetime.date | None = None,id: int | None = None):
        if club is not None:
            races = await db.execute(
                select(self.model).where(or_(*[self.model.homeClub == club, self.model.awayClub == club])))
            return races.scalars().all()
        if now is not None:
            races = await db.execute(select(self.model).where(self.model.startTime >= now))
            return races.scalars().all()
        if day is not None:
            races = await db.execute(select(self.model).where(func.date(self.model.startTime) == day))
            return races.scalars().all()
        if id is not None:
            races = await db.execute(select(self.model).where(self.model.id == id))
            return races.scalars().all()

    async def add_race(self, db: AsyncSession, obj: CreateRaceParam):
        new_start_time = obj.startTime
        new_end_time = obj.endTime

        # 查询时间区间是否与现有的时间区间重叠
        overlapping_intervals = await db.execute(
            select(self.model).where(
                or_(
                    and_(*[self.model.startTime < new_end_time, self.model.endTime >= new_end_time]),
                    and_(*[self.model.startTime <= new_start_time, self.model.endTime > new_start_time]),
                    and_(*[self.model.startTime >= new_start_time, self.model.endTime <= new_start_time])
                )
            )
        )

        # 获取结果
        overlapping_records = overlapping_intervals.scalars().all()

        # 如果 `overlapping_records` 不为空，则表示存在重叠
        if overlapping_records:
            return False, "存在时间冲突"
        else:
            dict_obj = obj.model_dump()
            new_race = self.model(**dict_obj)
            print(new_race)
            db.add(new_race)
            return True, "比赛创建成功"

    async def update_race(self, db, obj, id):
        try:
            new_start_time = obj['startTime']
            new_end_time = obj['endTime']
            overlapping_intervals = await db.execute(
                select(self.model).where(
                    or_(
                        and_(*[self.model.startTime < new_end_time, self.model.endTime >= new_end_time]),
                        and_(*[self.model.startTime <= new_start_time, self.model.endTime > new_start_time]),
                        and_(*[self.model.startTime >= new_start_time, self.model.endTime <= new_start_time])
                    )
                )
            )

            # 获取结果
            overlapping_records = overlapping_intervals.scalars().all()
            if overlapping_records:
                return False, "存在时间冲突"
        except:
            pass
        user = await db.execute(update(self.model).where(self.model.id == id).values(obj))
        if user.rowcount:
            return True
        else:
            return False


race_dao: CRUDRace = CRUDRace(Race)
