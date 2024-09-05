from typing import List

from app.crud.crud_matchplayer import matchplayer_dao
from app.crud.crud_race import race_dao
from schemas.matchplayer import CreateMatchPlayerParam
from schemas.race import *
from service.player_service import player_service
from service.user_service import user_service
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
    async def update_race(username: int, race: UpdateRaceParam):
        async with async_db_session.begin() as db:
            race_ = await race_dao.get_race(db=db, id=race.id)
            race_ = race_[0]
            oldawayClubId = race_.awayClubId
            oldhomeClubId = race_.homeClubId
            role = await user_dao.get(db=db, id=username)
            if not race.id:
                return False, "比赛 ID 不能为空"
            elif role[0].role // 1000 == 2:  # 2开头的为管理员,有所有权限
                dict = race.dict(exclude_unset=True)
                result = await race_dao.update_race(db=db, obj=dict, id=race.id)
                if race.awayClubId:
                    if oldawayClubId != race.awayClubId:
                        count = await matchplayer_dao.delete(db=db, raceId=race.id)
                if race.homeClubId:
                    if oldhomeClubId != race.homeClubId:
                        count = await matchplayer_dao.delete(db=db, raceId=race.id)
                return result, ''
            elif role[0].role // 100 == 11:  # 11开头的为队长
                if race.homeTeamGoalsScored or race.awayTeamGoalsScored:
                    return False, "队长不能修改比分"
                dict = race.dict(exclude_unset=True)
                result = await race_dao.update_race(db=db, obj=dict, id=race.id)
                if race.awayClubId:
                    if oldawayClubId != race.awayClubId:
                        count = await matchplayer_dao.delete(db=db,  raceId=race.id)
                if race.homeClubId:
                    if oldhomeClubId != race.homeClubId:
                        count = await matchplayer_dao.delete(db=db,  raceId=race.id)
                return result, ''

            else:
                return False, "权限不足"

    @staticmethod
    async def commit_player_list(list: List[CreateMatchPlayerParam], username: int, raceId: int | None = None):
        user = await user_service.get_user(id=username)
        user = user[0]
        if user.role // 1000 == 2 or user.role // 10 >= 100:
            async with async_db_session.begin() as db:
                for obj in list:
                    player = await player_service.get_player_by_userId(id=obj.userId)
                    if not obj.name:
                        obj.name = player[0].name
                    if not obj.clubId:
                        obj.clubId = player[0].clubId
                    if not obj.number:
                        obj.number = player[0].number
                    if not obj.position:
                        obj.position = player[0].position
                    result = await matchplayer_dao.create_matchplayer(db=db, obj=obj)
                return True, '添加成功'
        else:
            return False, '只有管理员和队长有此权限'


race_service = RaceService()
