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
    folder_path: pathlib.Path = Field(description='文件夹路径')
    algorithm: list[Literal['sha1', 'sha256','md5']] = Field(default=['sha256'], description='哈希算法')
    
    @model_validator(mode='before')
    @classmethod
    def model_post_init(cls, data):
        if isinstance(data, dict) and 'algorithm' in data:
            data['algorithm'] = [alg.lower() for alg in data['algorithm']]
        return data