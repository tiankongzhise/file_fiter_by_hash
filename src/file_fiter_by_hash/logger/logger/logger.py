from ...config.logger_config import LoggerConfig
import sys
from .schmeas import LoggerSchema
from ..db import LoggerRecord,LoggerWriter

class Logger:
    '''
    日志记录器
    使用方法：
    1. 创建Logger实例,需要日志名称
    2. 设置服务名称,必填,调用set_service方法
    3. 设置日志类型与状态映射关系(可选),默认debug至waring为success,error及以上为fail
    4. 设置额外信息与状态映射关系(可选),默认全部级别额外信息为""
    5. 记录日志,调用debug/info/warning/error/critical方法
    '''


    def __init__(self, name:str="default"):
        self.logger_name = name
        self.is_print_console = LoggerConfig.is_print_console
        self.is_persistence = LoggerConfig.is_persistence
        self.console_logger_level = LoggerConfig.console_logger_level
        self.persistence_logger_level = LoggerConfig.persistence_logger_level
        self.logger_level_map = LoggerConfig.logger_level_map
        self.writer = LoggerWriter().register().init_schema()

    def _get_call_info(self):

        """
        获取调用日志的代码位置信息
        return: (调用文件名称, 调用行号, 调用函数名)
        """
        # 获取调用栈的上一层帧（跳过当前的debug/info等日志方法，拿到业务代码的调用帧）
        frame = sys._getframe(3)
        # 获取调用的文件完整路径，用basename只保留文件名（比如：test.py，而不是/xxx/xxx/test.py）
        file_name = sys._getframe(3).f_code.co_filename.split("/")[-1]
        # 获取调用的代码行号
        line_no = frame.f_lineno
        # 获取调用的函数名，<module> 表示是在全局代码中调用（非函数内）
        func_name = frame.f_code.co_name
        return file_name, line_no, func_name
    
    def set_service(self, service_name:str):
        self.service_name = service_name

    def set_status_map(self, status_map:dict|None = None):
        self.status_map = status_map or {
            'debug':'success',
            'info':'success',
            'warning':'success',
            'error':'fail',
            'critical':'fail',
        }
    def set_extra_info_map(self, extra_info_map:dict|None = None):
        self.extra_info_map = extra_info_map or {
            'debug':'',
            'info':'',
            'warning':'',
            'error':'',
            'critical':'',
        }
    def set_logger_level_map(self, logger_level_map:dict):
        self.logger_level_map = logger_level_map

    
    def _is_console_output(self, logger_level:str):
        '''判断是否需要打印到控制台
        Args:
            logger_level (str): 日志级别
            
        Returns:
            bool: 是否需要打印到控制台
        '''
        return self.is_print_console and self.logger_level_map[logger_level] >= self.logger_level_map[self.console_logger_level]

    def _is_persistence_output(self, logger_level:str):
        '''判断是否需要持久化到数据库
        Args:
            logger_level (str): 日志级别
            
        Returns:
            bool: 是否需要持久化到数据库
        '''
        return self.is_persistence and self.logger_level_map[logger_level] >= self.logger_level_map[self.persistence_logger_level]
    
    def _validate_logger_input(self,logger_level:str,logger_message:str,call_info:str,status:str|None = None, extra_info:str|None = None):
        if not getattr(self, 'service_name'):
            raise ValueError('logger error service_name is required,set service_name by set_service method')
        if status is None:
            status = self.status_map[logger_level]
        if extra_info is None:
            extra_info = self.extra_info_map[logger_level]
        return LoggerSchema(logger_name = self.logger_name,logger_level=logger_level, logger_message=logger_message, service=self.service_name, status=status, extra_info=extra_info, call_info=call_info)

    @staticmethod
    def _to_dao(logger_input:LoggerSchema):
        return LoggerRecord(
            logger_name = logger_input.logger_name,
            logger_level = logger_input.logger_level,
            logger_message = logger_input.logger_message,
            service = logger_input.service,
            status = logger_input.status,
            extra_info = logger_input.extra_info,
            call_info = logger_input.call_info
        )

    def _log(self, logger_level:str, message:str, status:str|None = None, extra_info:str|None = None):
        file_name, line_no, func_name = self._get_call_info()
        call_path = f'{file_name}:{line_no}:{func_name}'
        if self._is_console_output(logger_level):
            print(f"{self.logger_name} -{logger_level}- {call_path}- {message}")
        if self._is_persistence_output(logger_level):
            validate_logger_input = self._validate_logger_input(logger_level, message, call_path, status, extra_info)
            self.writer.write(self._to_dao(validate_logger_input))

    def debug(self, message:str,status:str|None = None, extra_info:str|None = None):
        self._log('debug', message, status, extra_info)

    def info(self, message:str,status:str|None = None, extra_info:str|None = None):
        self._log('info', message, status, extra_info)

    def warning(self, message:str,status:str|None = None, extra_info:str|None = None):
        self._log('warning', message, status, extra_info)
    def error(self, message:str,status:str|None = None, extra_info:str|None = None):
        self._log('error', message, status, extra_info)
    def critical(self, message:str,status:str|None = None, extra_info:str|None = None):
        self._log('critical', message, status, extra_info)
