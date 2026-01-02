from sqlalchemy import create_engine
from .models import Base
from dotenv import load_dotenv
import os
load_dotenv('mysql.env')

class InitDB:
    _singleton = None
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton
    def __init__(self):
        self.user = os.getenv("MYSQL_USERNAME")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT")
        self.database = os.getenv("MYSQL_DATABASE")
        self.sslmode = os.getenv("MYSQL_SSLMODE")
        self.engine = None
    
    def init_db(self):
        if self.sslmode:
            DATABASE_URL  = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode={self.sslmode}"   
        else:
            DATABASE_URL  = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        print(DATABASE_URL)
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self._singleton = self

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
