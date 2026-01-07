from pydantic import BaseModel, Field, model_validator
from typing import Literal
import pathlib

class HashInfo(BaseModel):
    name: str
    # 限定为字符串file或folder
    type: Literal['file', 'folder']
    size: int
    hash_info:dict = Field(default={}, description='哈希信息')

class HashResult(BaseModel):
    status: Literal['success', 'error', 'empty','big_folder']
    info: HashInfo
    message: str = Field(default='', description='附加信息')

# 将algorithm转换为小写再比较
class HashParams(BaseModel):
    '''哈希参数
    args:
        item_path: 文件或文件夹路径
        algorithm: list[哈希算法] 可选值为sha1, sha256, md5
    '''
    item_path: pathlib.Path = Field(description='文件或文件夹路径')
    algorithm: list[Literal['sha1', 'sha256','md5']] = Field(default=['sha256'], description='哈希算法')
    
    @model_validator(mode='before')
    @classmethod
    def model_post_init(cls, data):
        if isinstance(data, dict) and 'algorithm' in data:
            data['algorithm'] = [alg.lower() for alg in data['algorithm']]
        return data

class FileOperationRecord(BaseModel):
    operation:Literal['remove','delete','zip']
    source_path:pathlib.Path = Field(description='源文件路径')
    target_path:pathlib.Path = Field(description='目标文件路径')
    file_name:str = Field(description='文件名')
    file_type:Literal['file','folder'] = Field(description='文件类型')
    hash_info:HashInfo = Field(description='哈希信息')
    operation_status:Literal['success','fail'] = Field(description='操作状态')
    error_message:str = Field(default='', description='错误信息')

class TempHashInfo(BaseModel):
    hash_tag:str = Field(description='哈希标签')
    name:str = Field(description='文件或文件夹名称')
    type:Literal['big_folder','folder','file'] = Field(description='文件类型')
    size:int = Field(description='文件大小')

class LoggerInfo(BaseModel):
    '''日志信息
    args:
        logger_level: 日志级别
        log_message: 日志消息
    logger_level将会被强制转化为小写，且必须在logger_level_map中
    '''
    logger_level:str = Field(description='日志级别')
    logger_call_path:str = Field(default='', description='日志调用路径')
    service_code:str = Field(default='', description='服务代码')
    log_message:str = Field(description='日志消息')
    
    @model_validator(mode='before')
    @classmethod
    def model_post_init(cls, data):
        if isinstance(data, dict) and 'logger_level' in data:
            from ..config.logger_config import LoggerConfig
            source_logger_level_input = data['logger_level']
            data['logger_level'] = data['logger_level'].lower()
            if data['logger_level'] not in LoggerConfig.logger_level_map:
                raise ValueError(f'logger_level {source_logger_level_input} is not valid')
        return data
