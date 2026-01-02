from sqlmodel import Session, SQLModel,create_engine
from .models import FileHashResult
from dotenv import load_dotenv
import os
load_dotenv()

class InitDB:
    _singleton = None
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton
    def __init__(self):
        self.user = os.getenv("PG_USERNAME")
        self.password = os.getenv("PG_PASSWORD")
        self.host = os.getenv("PG_HOST")
        self.port = os.getenv("PG_PORT")
        self.database = os.getenv("PG_DATABASE")
        self.sslmode = os.getenv("PG_SSLMODE")
        self.engine = None
    
    def init_db(self):
        DATABASE_URL  = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode={self.sslmode}"   
        self.engine = create_engine(DATABASE_URL)
        SQLModel.metadata.create_all(self.engine)
        self._singleton = self

    def get_engine(self):
        if not self.engine:
            self.init_db()
        return self.engine
    

def get_db_engine():
    print('run_init_db')
    init_db = InitDB()
    return init_db.get_engine()



