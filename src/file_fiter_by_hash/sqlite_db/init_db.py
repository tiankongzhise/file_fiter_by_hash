from sqlalchemy import create_engine
from .models import Base
import os

class InitDB:
    _singleton = None
    _is_init = False
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton
    def __init__(self):
        self.engine = None
    
    def init_db(self):
        if self._is_init:
            return 
        DATABASE_URL = 'sqllite:///local_sqllite_db.db'
        self.engine = create_engine(DATABASE_URL)
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
