from sqlalchemy import create_engine
from .models import Base
from dotenv import load_dotenv
import os

# 默认使用 SQLite，也可以配置 MySQL
load_dotenv()

class InitDB:
    _singleton = None
    _is_init = False

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self):
        if self._is_init:
            return
        # 优先使用 MySQL 配置，如果不存在则使用 SQLite
        self.mysql_user = os.getenv("MYSQL_USERNAME")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_host = os.getenv("MYSQL_HOST")
        self.mysql_port = os.getenv("MYSQL_PORT")
        self.mysql_database = os.getenv("MYSQL_DATABASE")
        self.mysql_sslmode = os.getenv("MYSQL_SSLMODE")

        # SQLite 配置
        self.sqlite_path = os.getenv("SQLITE_PATH", "data.db")

        self.engine = None

    def init_db(self):
        if self.mysql_user:
            # 使用 MySQL
            if self.mysql_sslmode:
                DATABASE_URL = f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?sslmode={self.mysql_sslmode}"
            else:
                DATABASE_URL = f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        else:
            # 使用 SQLite
            DATABASE_URL = f"sqlite:///{self.sqlite_path}"

        self.engine = create_engine(DATABASE_URL, echo=False)
        Base.metadata.create_all(self.engine)
        self._is_init = True

    def get_engine(self):
        if not self.engine:
            self.init_db()
        return self.engine

    def reset_db(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)


def get_db_engine():
    init_db = InitDB()
    return init_db.get_engine()


def reset_db():
    init_db = InitDB()
    init_db.get_engine()
    init_db.reset_db()
