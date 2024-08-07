from app.crud.crud_club import club_dao
from app.crud.crud_player import player_dao
from schemas.player import *
from util.token import *


class PlayerService:

    @staticmethod
    async def add_player(obj_in: CreatePlayerParam):
        async with async_db_session.begin() as db:
            data = await player_dao.get_player(db=db, userId=obj_in.userId)
            if data:
                return False, "该用户已有运动员"
            await player_dao.create_player(db=db, obj=obj_in)
            current_user = await user_dao.get(id=obj_in.userId, db=db)
            id = current_user[0].id
            await user_dao.update_userinfo(db, id=id, obj={"role": current_user[0].role + 1})
            return True, "球员创建成功"

    @staticmethod
    async def get_player_by_userId(id: str | int):
        async with async_db_session.begin() as db:
            player = await player_dao.get_player(db=db, userId=int(id))
            return player

    @staticmethod
    async def get_player_by_club(club: str):
        async with async_db_session.begin() as db:
            players = await player_dao.get_player(db=db, club=club)
            return players

    @staticmethod
    async def join_club(obj: UpdatePlayerParam, userId: int):
        async with async_db_session.begin() as db:
            player = await player_dao.get_player(db=db, userId=userId)
            club = await club_dao.get_club(db=db, name=obj.club)
            if player[0].flag:
                return False, "你已加入俱乐部，请先退出"
            if not player:
                return False, "该用户不存在"
            if not club:
                return False, "该俱乐部不存在"
            await player_dao.update_player(db, id=userId, obj={"club": obj.club, "flag": 0})
            return True, "申请成功"
    @staticmethod
    async def exit_club(obj: UpdatePlayerParam, userId: str | int):
        pass

    @staticmethod
    async def update_player(obj: UpdatePlayerParam, userId: int):
        async with async_db_session.begin() as db:
            player = await player_dao.get_player(db=db, userId=userId)
            if not player:
                return False, "该用户不存在"
            player_info = obj.dict(exclude_unset=True)
            await player_dao.update_player(db, id=userId, obj=player_info)
            return True, "信息修改成功"

player_service = PlayerService()
