from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar,Optional

T = TypeVar('T', bound=DeclarativeBase)


class SQLiteModelManager:
    '''
    Sqlite模型管理器，用于管理Sqlite模型,本身为单例模式
    通过模块名，将各模块的源数据注册到模型管理器中，方便后续调用
    register_model注册模型，get_model获取模型
    register_model:
    args:
        module_name: 模块名称,字符串类型,作为模型的key
        model: 模型类,继承自DeclarativeBase
    return:
        self
    register_model:
    args:
        module_name: 模块名称,字符串类型,作为模型的key
    return:
        model: 模型类,继承自DeclarativeBase
    '''
    _singleton = None
    _is_init = False
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(SQLiteModelManager, cls).__new__(cls, *args, **kwargs)
        return cls._singleton

    def __init__(self):
        if self._is_init:
            return
        self._is_init = True
        self.models = {}
    
    def register_model(self, module_name:str,model:T):
        self.models[module_name] = model
        return self
    
    def get_model(self, module_name:str)->T:
        if not self.models.get(module_name):
            raise ValueError(f"{module_name} 没有注册模型")
        return self.models.get(module_name)
