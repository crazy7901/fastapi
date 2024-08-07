import configparser  						# 导入的模块
from logging.config import fileConfig		# 导入的模块
from urllib.parse import quote_plus			# 导入的模块

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from db.models import User,Club						# 导入模块
target_metadata = User.metadata 				# 指定元数据
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
################################ 添加的内容 ################################
# 使用 configparser 读取另外一个.ini文件
config_parser = configparser.ConfigParser()
config_parser.read('config.ini')
host = config_parser.get('mysql', 'mysql_host')
user = config_parser.get('mysql', 'mysql_user')
password = quote_plus(config_parser.get('mysql', 'mysql_pass')).replace("%", "%%")
port = config_parser.get('mysql', 'mysql_port')
db = config_parser.get('mysql', 'mysql_db')
database_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
###########################################################################
config.set_main_option('sqlalchemy.url', database_url)	# 新增内容

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()