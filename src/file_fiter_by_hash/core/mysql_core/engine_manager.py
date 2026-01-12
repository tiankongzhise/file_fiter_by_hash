from sqlalchemy import create_engine


class MySQLEngineManager:
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
            cls._singleton = super(MySQLEngineManager, cls).__new__(cls, *args, **kwargs)
        return cls._singleton
    def __init__(self):
        if self._is_init:
            return
        self._is_init = True
        self.engine = {}
    
    def _get_engine_url(self, db_name:str|None):
        from dotenv import load_dotenv
        import os
        load_dotenv('mysql.env')
        host = os.getenv('MYSQL_HOST')
        port = os.getenv('MYSQL_PORT')
        password = os.getenv('MYSQL_PASSWORD')
        user_name = os.getenv('MYSQL_USERNAME')
        database = db_name or os.getenv('MYSQL_DATABASE')
        return f'mysql+pymysql://{user_name}:{password}@{host}:{port}/{database}'

    def register_engine(self,module_name:str, db_name:str=None, engine_config = None):
        # sqlalchemy使用pymysql连接mysql
        engine_url = self._get_engine_url(db_name)
        if engine_config:
            self.engine[module_name] = create_engine(engine_url, **engine_config)
        else:
            self.engine[module_name] = create_engine(engine_url)
        return self

    def get_engine_by_module(self, module_name:str):
        if not self.engine.get(module_name):
            raise ValueError(f"{module_name} 没有注册数据库引擎，请先注册引擎")
        return self.engine[module_name]

    def get_engine_by_db(self, db_name:str):
        try:
            engine_url =self._get_engine_url(db_name)
            engine = create_engine(engine_url)
            engine.connect()
            return engine
        except Exception as e:
            raise ValueError(f"{db_name}数据库连接异常,具体错误为{str(e)}")
