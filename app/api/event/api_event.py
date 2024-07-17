from fastapi import APIRouter
from common.response.response_schema import response_base

router = APIRouter()


@router.post('/add', summary="创建赛事")
async def addMatch():
    return await response_base.success()


@router.put('/update', summary="更新赛事信息")
async def updateMatch():
    return await response_base.success()


@router.get('/detail', summary="获取赛事详情")
async def getMatchDetail():
    return await response_base.success()


@router.delete('/delete', summary="注销赛事")
async def deleteMatch():
    return await response_base.success()


@router.post('/join', summary="邀请俱乐部参与")
async def joinClub():
    return await response_base.success()


