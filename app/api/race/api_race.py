from fastapi import APIRouter

from common.response.response_schema import response_base
from schemas.race import CreateRaceParam
from service.race_service import race_service

router = APIRouter()


@router.get("/next", summary="获取下一场比赛") # 未开始的赛事
async def getNextMatch():
    data = await race_service.get_next()
    if data:
        data = {
            "id": data.id,
            "startTime": data.startTime.strftime('%Y-%m-%d %H:%M:%S'),
            "endTime": data.endTime.strftime('%Y-%m-%d %H:%M:%S'),
            "homeClub": data.homeClub,
            "awayClub": data.awayClub,
            "venue": data.venue,
            "eventId": data.eventId,
            "multiPlayer": data.multiPlayer
        }
    return await response_base.success(data=data)


@router.get('/races', summary="获取今日赛事")  # 可能开始可能未开始，若不存在比分显示比赛未开始
async def getTodayMatches():
    datas = await race_service.get_today()
    races = []
    if datas:
        for data in datas:
            d = {
                "id": data.id,
                "startTime": data.startTime.strftime('%Y-%m-%d %H:%M:%S'),
                "endTime": data.endTime.strftime('%Y-%m-%d %H:%M:%S'),
                "homeClub": data.homeClub,
                "awayClub": data.awayClub,
                "venue": data.venue,
                "eventId": data.eventId,
                "multiPlayer": data.multiPlayer,
                "homeTeamGoalsScored": data.homeTeamGoalsScored,
                "awayTeamGoalsScored": data.awayTeamGoalsScored,
                "homeTeamJersey": data.homeTeamJersey,
                "awayTeamJersey": data.awayTeamJersey
            }
            races.append(d)
    return await response_base.success(data=races)


@router.get('/schedule', summary="获取本周赛程表")
async def getSchedule():
    return await response_base.success()


@router.get('/owner', summary="个人的赛事")
async def getOwnerMatch():
    return await response_base.success()


@router.post('/add', summary="创建比赛")
async def addMatch(race: CreateRaceParam):
    result = await race_service.add_race(race)
    if result[0]:
        return await response_base.success(data=result[1])
    else:
        return await response_base.fail(data=result[1])


@router.put('/update', summary="更新比赛")
async def updateMatch():
    return await response_base.success()


@router.get('/detail', summary="比赛详情")
async def getMatchDetail():
    return await response_base.success()


@router.delete('/delete', summary="取消比赛")
async def deleteMatch():
    return await response_base.success()


@router.post('/addgoal', summary="创建进球")
async def addGoal():
    return await response_base.success()
