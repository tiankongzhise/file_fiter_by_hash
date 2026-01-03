import pathlib
from typing import TypeVar
from sqlalchemy import Engine,select
from sqlalchemy.orm import DeclarativeBase,Session
from ..schmeas import FileOperationRecord
from ..utils.dto import trans_file_operation_dto_to_dao
from ..mysql_db import get_db_engine,FileOperationRecordTable

RecordTable = TypeVar('RecordTable', bound=DeclarativeBase)



class OperationRecording:
    '''
    将文件的操作日志记录到数据库中
    '''
        # 定义一个类属性，用来缓存唯一的实例
    __instance = None

    def __new__(cls, *args, **kwargs):
        # 核心判断：如果缓存中没有实例，就创建
        if cls.__instance is None:
            # 调用父类的__new__创建实例
            cls.__instance = super().__new__(cls)
        # 直接返回缓存的实例（永远同一个）
        return cls.__instance
        
    def __init__(self,db_engine:Engine=None,record_table:RecordTable=FileOperationRecordTable):
        self.engine = db_engine or get_db_engine()
        self.table = record_table

    def record(self,operation_record:FileOperationRecord):
        with Session(self.engine) as session:
            session.add(trans_file_operation_dto_to_dao(operation_record))
            session.commit()

__temp_operation_recording_item = OperationRecording()
recoding_file_operation = __temp_operation_recording_item.record
