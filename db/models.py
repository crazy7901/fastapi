from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, event
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, comment='id')
    email = Column(String(50), unique=True, index=True, comment="邮箱")
    password = Column(String(50), comment="密码")
    name = Column(String(50), unique=True, comment="名字")
    is_active = Column(Boolean, default=True, comment="状态")
    role = Column(Integer, default=1000,
                  comment="角色 1：队长 2：教练 3：队员,格式为1000，第二位为队长（球队创建者默认为队长），第三位位为教练，第四位为队员")
    clubId = Column(Integer, comment="俱乐部id")
    createdTime = Column(DateTime, default=datetime.now, comment="创建时间")
    # avatar = Column(Integer, default=0, comment="头像，0-11")
    # items = relationship("Club", back_populates="player")ateTime, server_default=func.now(), comment="创建时间")  #
    # 使用server_default owner_id=Mapper[]=mapped_column(Integer, index=True, comment="球队创建者")

    # 关系定义
    # players = relationship("Player", foreign_keys="Player.userId", backref="user")
    # clubs = relationship("Club", foreign_keys="Club.captain", backref="user")
    # transfers = relationship("Transfer", foreign_keys="Transfer.userId", backref="user")
    # goals = relationship("Goal", foreign_keys="Goal.userId", backref="user")
    # events = relationship("Events", foreign_keys="Events.userId", backref="user")


class Club(Base):
    __tablename__ = "clubs"

    captain = Column(Integer, ForeignKey('users.id'), comment='用户名')
    id = Column(Integer, primary_key=True, index=True, comment="id")
    name = Column(String(50), index=True, comment="俱乐部名")
    # avatar = Column(Integer, default=0, comment="头像，0-11")
    # owner = relationship("player", back_populates="Club")
    createdTime = Column(DateTime, default=datetime.now, comment="创建时间")


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, comment='id')
    number = Column(Integer, unique=True, index=True, comment="球队号码")
    clubId = Column(Integer, ForeignKey('clubs.id'), comment="俱乐部名")
    position = Column(String(50), comment="场上位置")
    name = Column(String(50), comment="球员名")
    userId = Column(Integer, comment='用户名')
    # goalsScoredInFriendlies = Column(Integer, comment='友谊赛进球数')
    # goalsScoredInChallenges = Column(Integer, comment='正赛赛进球数')
    createdTime = Column(DateTime, default=datetime.now, comment="创建时间")
    flag = Column(Integer, default=0, comment='球员状态,0为尚未通过审核,1为正式球员')


class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True, comment='id')
    formatNumber = Column(Integer, unique=True, index=True, comment="旧球队号码")
    formatClub = Column(Integer, ForeignKey('clubs.id'),comment="原俱乐部id")
    newNumber = Column(Integer, unique=True, index=True, comment="新球队号码")
    newClub = Column(Integer, ForeignKey('clubs.id'), comment="现俱乐部id")
    userId = Column(Integer, ForeignKey('users.id'), comment='用户id')
    createdTime = Column(DateTime, default=datetime.now, comment="转会时间")


class Race(Base):
    __tablename__ = "races"
    id = Column(Integer, primary_key=True, comment='id')
    startTime = Column(DateTime, comment="比赛开始时间")
    endTime = Column(DateTime, comment="比赛结束时间")
    homeClubId = Column(Integer, ForeignKey('clubs.id'), comment="主队")
    awayClubId = Column(Integer, ForeignKey('clubs.id'), comment="客队")
    homeTeamJersey = Column(String(50), comment='主场球衣颜色')
    awayTeamJersey = Column(String(50), comment='客场球衣颜色')
    multiPlayer = Column(Integer, comment='多人制')
    venue = Column(Integer, comment='1、金盆岭左半场 2、金盆岭右半场 3、云塘左半场 4、云塘右半场')
    eventId = Column(Integer, default=0, comment="比赛类型：某锦标赛、友谊赛=0等")
    createdTime = Column(DateTime, default=datetime.now, comment="比赛创建时间")
    homeTeamGoalsScored = Column(Integer, comment="主队进球数")
    awayTeamGoalsScored = Column(Integer, comment="客队进球数")
    userId = Column(Integer, ForeignKey('users.id'), comment='创建者id')


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, comment='id')
    raceId = Column(Integer, comment='比赛id')
    userId = Column(Integer, ForeignKey('users.id'), comment='进球球员用户名')
    eventId = Column(Integer, default=0, comment="比赛类型：某锦标赛、友谊赛=0等")
    goalTime = Column(String(50), comment="进球时间")
    goalType = Column(Integer, default=0, comment="0运动战进球，1任意球，2点球,3黄牌，4红牌,5助攻")
    clubId = Column(Integer, ForeignKey('clubs.id'), comment="球员所属俱乐部id")
    scoredClub = Column(Integer, ForeignKey('users.id'), comment="被进球的俱乐部id")


class Events(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, comment='id')
    userId = Column(Integer, ForeignKey('users.id'), comment='赛事创建者')
    type = Column(Integer, comment="赛事类型0联赛，1杯赛")
    multiPlayer = Column(Integer, comment='多人制')


class MatchPlayers(Base):
    __tablename__ = "matchplayers"
    id = Column(Integer, primary_key=True, comment='id')
    number = Column(Integer, unique=True, index=True, comment="球队号码")
    clubId = Column(Integer, ForeignKey('clubs.id'), comment="俱乐部id")
    position = Column(String(50), comment="场上位置")
    name = Column(String(50), comment="球员名")
    userId = Column(Integer, ForeignKey('users.id'), comment='用户名')
    raceId = Column(Integer, ForeignKey('races.id'), comment='比赛id')
    # goalsScoredInFriendlies = Column(Integer, comment='友谊赛进球数')
    # goalsScoredInChallenges = Column(Integer, comment='正赛赛进球数')
    # createdTime = Column(DateTime, default=datetime.now, comment="创建时间")
    # flag = Column(Integer, default=0, comment='球员状态,0为尚未通过审核,1为正式球员')
# 
# async def update_player_name(mapper, connection, target):
#     # Update the player's name and userId when the User object is updated
#     try:
#         for player in target.players:
#             print("修改成功")
#             # player.name = target.name
#             player.userId = target.name
#     except:
#         print("无player对象")
# 
#     try:
#         for club in target.clubs:
#             club.captain = target.name
#     except:
#         print("无club对象")
# 
#     try:
#         for transfer in target.transfers:
#             transfer.userId = target.name
#     except:
#         print("无transfer对象")
# 
#     try:
#         for goal in target.goals:
#             goal.userId = target.name
#     except:
#         print("无goal对象")
# 
#     try:
#         for event in target.events:
#             event.userId = target.name
#     except:
#         print("无event对象")
# 
# # Listen for the 'after_update' event on the User class
# event.listen(User, 'after_update', update_player_name)
