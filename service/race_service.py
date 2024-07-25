from app.crud.crud_race import race_dao
from schemas.race import *
from util.token import *


class RaceService:

    @staticmethod
    async def get_next():
        async with async_db_session.begin() as db:
            now = datetime.datetime.now()
            try:
                race = await race_dao.get_race(db=db, now=now)
                # race.start_time = race.start_time.strftime('%Y-%m-%d %H:%M:%S')
                # race.end_time = race.end_time.strftime('%Y-%m-%d %H:%M:%S')
                race = race[0]
            except:
                race = None
            return race

    @staticmethod
    async def get_today():
        async with async_db_session.begin() as db:
            today = datetime.date.today()
            try:
                race = await race_dao.get_race(db=db, day=today)
                # race = race[0]
            except:
                race = None
            return race

    @staticmethod
    async def add_race(race: CreateRaceParam):
        async with async_db_session.begin() as db:
            result = await race_dao.add_race(db=db, obj=race)
            return result

    @staticmethod  # 队长可以修改比赛时间，
    async def update_race(username: str, race: UpdateRaceParam):
        async with async_db_session.begin() as db:
            role = await user_dao.get(db=db,name=username)
            if not race.id:
                return False, "比赛 ID 不能为空"
            if role[0].role // 1000 == 2:  # 2开头的为管理员,有所有权限
                dict = race.dict(exclude_unset=True)
                result = await race_dao.update_race(db=db, obj=dict, id=race.id)
                return result,''
            if role[0].role // 100 == 11:  # 2开头的为管理员
                if race.homeTeamGoalsScored or race.awayTeamGoalsScored:
                    return False, "队长不能修改比分"
                dict = race.dict(exclude_unset=True)
                result = await race_dao.update_race(db=db, obj=dict,id=race.id)
                return result,''
            else:
                return False, "权限不足"



race_service = RaceService()
