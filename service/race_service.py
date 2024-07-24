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


race_service = RaceService()
