from app.crud.crud_club import club_dao
from app.crud.crud_user import user_dao
from db.database import async_db_session
from schemas.club import CreateClubParam


class ClubService:

    @staticmethod
    async def create_club(club: CreateClubParam, creator: str):
        # 实现 club 创建功能
        async with async_db_session.begin() as db:
            user = await user_dao.get(db=db, name=creator)
            current_club = await club_dao.get_club(db=db, name=club.name)
            user = user[0]
            role = user.role
            if role != 1000:  # 说明已为某队队员，不可创建球队
                return False, '已加入俱乐部，不可创建'
            elif current_club:
                return False, '俱乐部名重复'
            else:
                # 实现 club 创建功能
                club.captain = user.id
                await club_dao.create_club(db=db, obj=club)
                await user_dao.update_userinfo(db=db, id=user.id, obj={"role": 1100})
                clubs = await club_dao.get_club(db=db, name=club.name)
                return True, clubs[0]


club_service = ClubService