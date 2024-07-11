from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Mapper, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, comment='id')
    email = Column(String(50), unique=True, index=True, comment="邮箱")
    password = Column(String(50), comment="密码")
    name = Column(String(50), comment="名字")
    is_active = Column(Boolean, default=True, comment="状态")
    role = Column(Integer, default=1000,comment="角色 1：队长 2：教练 3：队员,格式为1000，第二位为队长（球队创建者默认为队长），第三位位为教练，第四位为队员")
    club = Column(String(50), index=True, comment="所属球队名", default=None)
    avatar = Column(Integer, default=0,comment="头像，0-11")
    # items = relationship("Club", back_populates="player")ateTime, server_default=func.now(), comment="创建时间")  #
    # 使用server_default owner_id=Mapper[]=mapped_column(Integer, index=True, comment="球队创建者")


class Club(Base):
    __tablename__ = "clubs"

    captain = Column(Integer, index=True, comment="队长id")
    id = Column(Integer, primary_key=True, index=True, comment="id")
    name = Column(String(50), index=True, comment="俱乐部名")
    avatar = Column(Integer, default=0, comment="头像，0-11")
    # owner = relationship("player", back_populates="Club")
