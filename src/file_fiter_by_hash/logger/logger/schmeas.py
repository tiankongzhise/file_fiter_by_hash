from pydantic import BaseModel,field_validator
from typing import Any
from ...config.logger_config import LoggerConfig

class LoggerSchema(BaseModel):
    logger_name: str
    logger_level: str
    logger_message:str
    service: str
    status: str
    extra_info: str
    call_info: str

@field_validator('logger_level')
@classmethod
def validate_logger_level(cls,v:Any):
    if v not in LoggerConfig.logger_level_map.keys():
        raise ValueError('logger_level must be one of {}'.format(LoggerConfig.logger_level_map))
    return v

@field_validator('status')
@classmethod
def validate_logger_status(cls,v:Any):
    if v not in LoggerConfig.logger_status:
        raise ValueError('status must be one of {}'.format(LoggerConfig.logger_status))
    return v

