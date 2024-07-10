from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from core.Setting import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./db.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/fba"
SQLALCHEMY_DATABASE_URL = (f'mysql+asyncmy://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:'
                        f'{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset={settings.MYSQL_CHARSET}')
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

Base = declarative_base()

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker


# 数据库连接初始化
def create_engine_and_session(url: str | URL):
    # 创建mysql连接引擎
    try:
        engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True, pool_pre_ping=True)
    except Exception as e:
        raise ConnectionError('数据库连接失败')
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session


async_engine, async_db_session = create_engine_and_session(SQLALCHEMY_DATABASE_URL)
