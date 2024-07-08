from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Mapper, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id: Mapper[int] = mapped_column(init=False)
    email : Mapper[str]=mapped_column(String(50), unique=True, index=True, comment="邮箱")
    password : Mapper[str]=mapped_column(String(50), comment="密码")
    name : Mapper[str]=mapped_column(String(50), comment="名字")
    is_active : Mapper[bool]=mapped_column(Boolean, default=True, comment="状态")
    role : Mapper[int]=mapped_column(Integer, comment="角色 1：队长 2：教练 3：队员")
    number : Mapper[int]=mapped_column(Integer, comment='球衣号码')
    club : Mapper[str]=mapped_column(String(50), index=True, comment="所属球队名", default=None)
    # items = relationship("Club", back_populates="player")ateTime, server_default=func.now(), comment="创建时间")  # 使用server_default
    #     owner_id : Mapper[]=mapped_column(Integer, index=True, comment="球队创建者")


class Club(Base):
    __tablename__ = "clubs"

    id : Mapper[int]=mapped_column(Integer, primary_key=True, index=True, comment="id")
    # owner = relationship("player", back_populates="Club")
