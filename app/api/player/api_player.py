from fastapi import APIRouter
from common.response.response_schema import response_base

router = APIRouter()


@router.post('/add', summary="创建球员")
async def addMatch():
    return await response_base.success()


@router.put('/update', summary="更新球员信息")
async def updateMatch():
    return await response_base.success()


@router.get('/detail', summary="获取球员详情")
async def getMatchDetail():
    return await response_base.success()


@router.delete('/delete', summary="注销球员")
async def deleteMatch():
    return await response_base.success()


@router.post('/join', summary="申请加入俱乐部")
async def joinClub():
    return await response_base.success()


