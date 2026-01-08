from .model import LoggerModelBase
from ...core.sqlite_core import SQLiteEngineManager,SQLiteModelManager,SQLiteSchemaManager,T
from sqlalchemy.orm import Session


class LoggerWriter(object):
    def __init__(self):
        self.engine_manager = SQLiteEngineManager()
        self.model_manager = SQLiteModelManager()
        self.schema_manager = SQLiteSchemaManager()
    
    def register(self):
        self.engine_manager.register_engine('logger', 'logger')
        self.model_manager.register_model('logger', LoggerModelBase)
        return self
    def init_schema(self):
        self.schema_manager.init_schema('logger')
        return self
    def write(self, data:T):
        engine = self.engine_manager.get_engine_by_module('logger')
        with Session(engine) as session:
            session.add(data)
            result = session.commit()
            return result
