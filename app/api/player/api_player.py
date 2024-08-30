from fastapi import APIRouter
from fastapi.params import Depends

from app.crud.crud_club import club_dao
from common.response.response_schema import response_base
from db.database import async_db_session
from schemas.player import CreatePlayerParam, UpdatePlayerParam
from service.player_service import player_service
from util.token import get_current_token

router = APIRouter()


@router.post('/add', summary="创建球员")
async def addPlayer(player: CreatePlayerParam, current_user: dict = Depends(get_current_token)):
    username = current_user['username']
    player.userId = username
    data = await player_service.add_player(obj_in=player)
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])


@router.put('/update', summary="更新球员信息")
async def update(obj: UpdatePlayerParam, current_user: dict = Depends(get_current_token)):
    return await response_base.success()


@router.get('/detail', summary="获取球员详情（球员卡）")
async def getPlayerDetail(current_user: dict = Depends(get_current_token)):
    detail = await player_service.get_player_by_userId(id=current_user['username'])
    playDetail = detail[0]
    data = {'number': playDetail.number,
            'name': playDetail.name,
            'position': playDetail.position
            }
    if playDetail.flag:
        async with async_db_session.begin() as db:
            club = await club_dao.get_club(db=db, id=playDetail.clubId)
            data['club'] = club[0].name
    else:
        data['club'] = '未加入俱乐部'
    return await response_base.success(data=data)


@router.delete('/delete', summary="注销球员")
async def deletePlayer(current_user: dict = Depends(get_current_token)):
    return await response_base.success()


@router.post('/join', summary="申请加入俱乐部")
async def joinClub(obj: UpdatePlayerParam, current_user: dict = Depends(get_current_token)):
    username = current_user['username']
    data = await player_service.join_club(userId=username, obj=obj)
    if data[0]:
        return await response_base.success(data=data[1])
    else:
        return await response_base.fail(data=data[1])
