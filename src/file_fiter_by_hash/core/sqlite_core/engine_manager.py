from sqlalchemy import create_engine
import pathlib

class SQLiteEngineManager:
    '''
    SQLite 引擎管理,单例类,
    实例对象调用register_engine注册数据库引擎,调用get_engine获取数据库引擎
    register_engine调用参数
    args:
        module_name: 模块名称,字符串类型,作为数据库引擎的key
        db_name: 数据库名称,字符串类型,作为数据库文件名
        engine_config: 数据库引擎配置,字典类型,作为create_engine参数
    return:
        self: 当前对象
    
    get_engine调用参数
    args:
        module_name: 模块名称,字符串类型,作为数据库引擎的key
    return:
        engine: 数据库引擎
    '''
    _singleton = None
    _is_init = False
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(SQLiteEngineManager, cls).__new__(cls, *args, **kwargs)
        return cls._singleton
    def __init__(self):
        if self._is_init:
            return
        self._is_init = True
        self.engine = {}
    
    def register_engine(self,module_name:str, db_name:str, engine_config = None):
        if engine_config:
            self.engine[module_name] = create_engine(f'sqlite:///{db_name}.db', **engine_config)
        else:
            self.engine[module_name] = create_engine(f'sqlite:///{db_name}.db')
        return self

    def get_engine_by_module(self, module_name:str):
        if not self.engine.get(module_name):
            raise ValueError(f"{module_name} 没有注册数据库引擎，请先注册引擎")
        return self.engine[module_name]

    def get_engine_by_db(self, db_name:str):
        if not pathlib.Path(f'{db_name}.db').exists():
            raise ValueError(f"{db_name}数据库不存在,请先注册数据库")
        engine = create_engine(f'sqlite:///{db_name}.db')
        return engine
