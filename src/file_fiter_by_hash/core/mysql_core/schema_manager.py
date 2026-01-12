from .engine_manager import MySQLEngineManager
from .model_manager import MySQLModelManager,T


class MySQLSchemaManager:
    '''SQLite Schema管理,单例类,
    实例对象调用init_schema初始化数据库表结构,调用drop_schema删除数据库表结构
    init_schema调用参数
    @param module_name: 模块名称,字符串类型,作为数据库引擎的key
    drop_schema调用参数
    @param module_name: 模块名称,字符串类型,作为数据库引擎的key
    '''
    _singleton = None
    _is_init = False
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(MySQLSchemaManager, cls).__new__(cls, *args, **kwargs)
        return cls._singleton
    def __init__(self):
        if self._is_init:
            return
        self._is_init = True
        self.model_manager = MySQLModelManager()
        self.engine_manager = MySQLEngineManager()
    
    def set_model_manager(self, model_manager):
        self.model_manager = model_manager
    def set_engine_manager(self, engine_manager):
        self.engine_manager = engine_manager
    
    def init_schema(self, module_name:str):
        schema: T = self.model_manager.get_model(module_name)
        engine = self.engine_manager.get_engine_by_module(module_name)
        if not schema:
            raise ValueError(f"{module_name} 没有注册模型")
        if not engine:
            raise ValueError(f"{module_name} 没有注册数据库引擎，请先注册引擎")
        schema.metadata.create_all(engine)
    def drop_schema(self, module_name:str):
        schema: T = self.model_manager.get_model(module_name)
        engine = self.engine_manager.get_engine_by_module(module_name)
        if not schema:
            raise ValueError(f"{module_name} 没有注册模型")
        if not engine:
            raise ValueError(f"{module_name} 没有注册数据库引擎，请先注册引擎")
        schema.metadata.drop_all(engine)

    def reset_schema(self, module_name:str):
        self.drop_schema(module_name)
        self.init_schema(module_name)

    def create_table(self, module_name:str, model:T):
        engine = self.engine_manager.get_engine_by_module(module_name)
        schema:T = self.model_manager.get_model(module_name)
        schema.metadata.create_all(engine, [model.__table__])
    def drop_table(self, module_name:str, model:T):
        engine = self.engine_manager.get_engine_by_module(module_name)
        schema:T = self.model_manager.get_model(module_name)
        schema.metadata.drop_all(engine, [model.__table__])

