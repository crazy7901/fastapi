from typing import List

import oss2
from fastapi import APIRouter, Request
from fastapi.params import Depends
from oss2.credentials import EnvironmentVariableCredentialsProvider

from common.response.response_schema import response_base
from schemas.matchplayer import CreateMatchPlayerParam
from schemas.race import CreateRaceParam, UpdateRaceParam
from service.club_service import club_service
from service.race_service import race_service
from util.token import get_current_token

# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称，例如examplebucket。
bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'victory-greens')

# 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。
router = APIRouter()


@router.get("/next", summary="获取下一场比赛")  # 未开始的赛事
async def getNextMatch():
    data = await race_service.get_next()
    if data:
        homeClub=await club_service.get_club(data.homeClubId)
        awayClub=await club_service.get_club(data.awayClubId)
        object_name1 = f'club/{data.homeClubId}.png'
        url1 = bucket.sign_url('GET', object_name1, 3600, slash_safe=True)
        object_name2 = f'club/{data.awayClubId}.png'
        url2 = bucket.sign_url('GET', object_name2, 3600, slash_safe=True)
        data = {
            "id": data.id,
            "startTime": data.startTime.strftime('%Y-%m-%d %H:%M:%S'),
            "endTime": data.endTime.strftime('%Y-%m-%d %H:%M:%S'),
            "homeClub": homeClub.name,
            "awayClub": awayClub.name,
            "venue": data.venue,
            "eventId": data.eventId,
            "multiPlayer": data.multiPlayer,
            "homeAvatar": url1,
            "awayAvatar": url2
        }
    return await response_base.success(data=data)


@router.get('/races', summary="获取今日赛事")  # 可能开始可能未开始，若不存在比分显示比赛未开始
async def getTodayMatches():
    datas = await race_service.get_today()
    races = []
    if datas:
        for data in datas:
            homeClub=await club_service.get_club(data.homeClubId)
            awayClub=await club_service.get_club(data.awayClubId)
            object_name1 = f'club/{data.homeClubId}.png'
            url1 = bucket.sign_url('GET', object_name1, 3600, slash_safe=True)
            object_name2 = f'club/{data.awayClubId}.png'
            url2 = bucket.sign_url('GET', object_name2, 3600, slash_safe=True)
            d = {
                "id": data.id,
                "startTime": data.startTime.strftime('%Y-%m-%d %H:%M:%S'),
                "endTime": data.endTime.strftime('%Y-%m-%d %H:%M:%S'),
                "homeClub": homeClub.name,
                "awayClub": awayClub.name,
                "venue": data.venue,
                "eventId": data.eventId,
                "multiPlayer": data.multiPlayer,
                "homeAvatar": url1,
                "awayAvatar": url2
            }
            races.append(d)
    return await response_base.success(data=races)


@router.get('/schedule', summary="获取本周赛程表")
async def getSchedule():
    return await response_base.success()


@router.get('/owner', summary="个人所在俱乐部的赛事")
async def getOwnerMatch():
    return await response_base.success()


@router.post('/add', summary="创建比赛")
async def addMatch(race: CreateRaceParam, current_user: dict = Depends(get_current_token)):
    race.userId = current_user['username']
    result = await race_service.add_race(race)
    if result[0]:
        return await response_base.success(data=result[1])
    else:
        return await response_base.fail(data=result[1])


@router.put('/update', summary="更新比赛")
async def updateMatch(race: UpdateRaceParam, current_user: dict = Depends(get_current_token)):
    data = await race_service.update_race(username=current_user['username'], race=race)
    return await response_base.success()


@router.get('/detail', summary="比赛详情,包括球员信息")
async def getMatchDetail():
    return await response_base.success()


@router.delete('/delete', summary="取消比赛")
async def deleteMatch():
    return await response_base.success()


@router.post('/addgoal', summary="创建进球/违规")
async def addGoal():
    return await response_base.success()


# class IdsModel(BaseModel):
#     ids: CreateMatchPlayerParam
@router.post('/commit', summary="提交球员名单")
async def commitPlayerList(list: List[CreateMatchPlayerParam], request: Request,
                           current_user: dict = Depends(get_current_token)):
    # raceId = request.headers['id']
    # result = await race_service.commit_player_list(list=list, raceId=raceId)
    result = await race_service.commit_player_list(list=list, username=current_user['username'])
    if result[0]:
        return await response_base.success(data=result[1])
    else:
        return await response_base.fail(data=result[1])
