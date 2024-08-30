from pydantic import BaseModel

from app.crud.crud_club import club_dao
from app.crud.crud_player import player_dao
from app.crud.crud_user import user_dao
from db.database import async_db_session
from schemas.club import CreateClubParam


class PlayerUser(BaseModel):
    userId: int
    decision: int


class ClubService:

    @staticmethod
    async def create_club(club: CreateClubParam, creator: str | int):
        # 实现 club 创建功能
        async with async_db_session.begin() as db:
            user = await user_dao.get(db=db, id=int(creator))  # 用于验证创建人信息
            current_club = await club_dao.get_club(db=db, name=club.name)  # 用于查找俱乐部是否已存在
            player = await player_dao.get_player(db=db, userId=creator)
            user = user[0]
            role = user.role
            if role % 10 != 1:  # 只有尚未成为队长的球员
                return False, '尚未注册身份，不可创建'
            elif current_club:
                return False, '俱乐部名重复'
            elif player[0].flag:
                return False, '该用户已加入俱乐部'
            else:
                # 实现 club 创建功能
                club.captain = user.id
                await club_dao.create_club(db=db, obj=club)
                await user_dao.update_userinfo(db=db, id=user.id, obj={"role": role + 100})
                # await player_dao.update_player(db=db, id=creator, obj={"club": club.name, "flag": 1})
                clubs = await club_dao.get_club(db=db, name=club.name)
                return True, clubs[0]

    @staticmethod
    async def club_decide(playerinfo: PlayerUser, creator: int):
        async with async_db_session.begin() as db:
            current_user = await user_dao.get(db=db, id=creator)
            current_user = current_user[0]
            if current_user.role // 100 == 11:
                flag = playerinfo.decision
                userId = playerinfo.userId
                if flag:
                    await user_dao.update_userinfo(db=db, id=userId, obj={'clubId': current_user.clubId})
                    await player_dao.update_player(db=db, id=userId, obj={'clubId': current_user.clubId, 'flag': 1})
                    # send_message(msg="你已加入俱乐部***")
                else:
                    await player_dao.update_player(db=db, id=userId, obj={'clubId': None, 'flag': 0})
                    # send_message(msg="你的申请被拒绝")
                return True, "审核成功"
            else:
                return False, '只有队长可以执行此操作'


#

club_service = ClubService
