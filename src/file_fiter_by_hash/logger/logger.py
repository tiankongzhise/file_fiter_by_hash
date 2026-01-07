import sys
from .sqlite_db import sql_logger_write,reset_db
from ..schmeas import LoggerInfo
from ..config import LoggerConfig
from ..config.service_code import get_service_code_map

class Logger:
    _singleton = None
    _is_init = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton
    
    def __init__(self, logger_config:LoggerConfig = None):
        if self._is_init:
            return
        if not logger_config:
            logger_config = LoggerConfig()
        self.is_print_console = logger_config.is_print_console
        self.is_persistence = logger_config.is_persistence
        self.is_call_path = logger_config.is_call_path
        self.console_logger_level = logger_config.console_logger_level
        self.persistence_logger_level = logger_config.persistence_logger_level
        self.level_map = logger_config.logger_level_map
        
        self._is_init = True    

    def _validate_logger_config_value(self,attr_name:str,value:any):
        if attr_name == 'is_print_console' or attr_name == 'is_persistence':
            if not isinstance(value, bool):
                print(f'Logger object attribute {attr_name} must be bool type')
                return False
            return True
        elif attr_name == 'is_call_path':
            if not isinstance(value, bool):
                print(f'Logger object attribute {attr_name} must be bool type')
                return False
            return True
        elif attr_name == 'console_logger_level' or attr_name == 'persistence_logger_level':
            if not isinstance(value, str):
                print(f'Logger object attribute {attr_name} must be str type')
                return False
            if value.lower() not in self.level_map:
                print(f'Logger object attribute {attr_name} must be in {self.level_map.keys()}')
                return False
            return True
        
    
    def set_logger_config(self, **kwargs):
        '''设置日志配置 不会对输入进行校验，可以在运行时调整logger的各项设置
        Args:
            attr_name (str): 属性名
            value (str): 属性值
            
        Returns:
            None
        '''
        for attr_name, value in kwargs.items():
            if not hasattr(self, attr_name):
                print(f'Logger object has no attribute {attr_name}')
                return None
            if not self._validate_logger_config_value(attr_name, value):
                print(f'Logger object attribute {attr_name} value {value} is invalid,nothing will be done')
                return None
            if attr_name == 'console_logger_level' or attr_name == 'persistence_logger_level':
                value = value.lower()
            setattr(self, attr_name, value)

    def _is_console_output(self, logger_level:str):
        '''判断是否需要打印到控制台
        Args:
            logger_level (str): 日志级别
            
        Returns:
            bool: 是否需要打印到控制台
        '''
        return self.is_print_console and self.level_map[logger_level] >= self.level_map[self.console_logger_level]

    def _is_persistence_output(self, logger_level:str):
        '''判断是否需要持久化到数据库
        Args:
            logger_level (str): 日志级别
            
        Returns:
            bool: 是否需要持久化到数据库
        '''
        return self.is_persistence and self.level_map[logger_level] >= self.level_map[self.persistence_logger_level]
    
        # ============ 核心新增：获取调用日志的【文件+行号+函数名】 ============
    def _get_call_info(self):
        """
        获取调用日志的代码位置信息
        return: (调用文件名称, 调用行号, 调用函数名)
        """
        # 获取调用栈的上一层帧（跳过当前的debug/info等日志方法，拿到业务代码的调用帧）
        frame = sys._getframe(2)
        # 获取调用的文件完整路径，用basename只保留文件名（比如：test.py，而不是/xxx/xxx/test.py）
        file_name = sys._getframe(2).f_code.co_filename.split("/")[-1]
        # 获取调用的代码行号
        line_no = frame.f_lineno
        # 获取调用的函数名，<module> 表示是在全局代码中调用（非函数内）
        func_name = frame.f_code.co_name
        return file_name, line_no, func_name
    @staticmethod
    def _is_first_char_letter(text):
        import re
        pattern = r'^[A-Za-z]'
        return bool(re.match(pattern, text))
    
    def _get_service_code(self,code:str):
        # 写一个正则匹配code的第一位是否是26个字母
        temp = get_service_code_map().get(code.upper())
        if not temp:
            raise ValueError(f'service code {code} not defined in service code map')
        if self._is_first_char_letter(temp):
            return temp
        else:
            return code
        

    
    def debug(self,code:str,message:str):
        '''调试日志
        Args:
            message (str): 日志消息
            
        Returns:
            None
        '''
        code = self._get_service_code(code)
        call_path = ''
        if self.is_call_path:
            file_name, line_no, func_name = self._get_call_info()
            call_path = f'{file_name}:{line_no}:{func_name}'
        if self._is_console_output('debug'):
            print(f'DEBUG: {call_path}:{message}')
        if self._is_persistence_output('debug'):
            sql_logger_write(LoggerInfo(logger_level='debug', logger_call_path=call_path, service_code=code, log_message=message))
        
    def info(self,code:str,message:str):
        '''信息日志
        Args:
            message (str): 日志消息
            
        Returns:
            None
        '''
        code = self._get_service_code(code)
        call_path = ''
        if self.is_call_path:
            file_name, line_no, func_name = self._get_call_info()
            call_path = f'{file_name}:{line_no}:{func_name}'
        if self._is_console_output('info'):
            print(f'INFO: {call_path}:{message}')
        if self._is_persistence_output('info'):
            sql_logger_write(LoggerInfo(logger_level='info', logger_call_path=call_path, service_code=code, log_message=message))

    def warning(self,code:str,message:str):
        '''警告日志
        Args:
            message (str): 日志消息
            
        Returns:
            None
        '''
        code = self._get_service_code(code)
        call_path = ''
        if self.is_call_path:
            file_name, line_no, func_name = self._get_call_info()
            call_path = f'{file_name}:{line_no}:{func_name}'
        if self._is_console_output('warning'):
            print(f'WARNING: {call_path}:{message}')
        if self._is_persistence_output('warning'):
            sql_logger_write(LoggerInfo(logger_level='warning', logger_call_path=call_path, service_code=code, log_message=message))
        
    def error(self,code:str,message:str):
        '''错误日志
        Args:
            message (str): 日志消息
            
        Returns:
            None
        '''
        code = self._get_service_code(code)
        call_path = ''  
        if self.is_call_path:
            file_name, line_no, func_name = self._get_call_info()
            call_path = f'{file_name}:{line_no}:{func_name}'
        if self._is_console_output('error'):
            print(f'ERROR: {call_path}:{message}')
        if self._is_persistence_output('error'):
            sql_logger_write(LoggerInfo(logger_level='error', logger_call_path=call_path, service_code=code, log_message=message))
        
    def critical(self,code:str,message:str):
        '''严重错误日志
        Args:
            message (str): 日志消息
            
        Returns:
            None
        '''
        code = self._get_service_code(code)
        call_path = ''
        if self.is_call_path:
            file_name, line_no, func_name = self._get_call_info()
            call_path = f'{file_name}:{line_no}:{func_name}'
        if self._is_console_output('critical'):
            print(f'CRITICAL: {call_path}:{message}')
        if self._is_persistence_output('critical'):
            sql_logger_write(LoggerInfo(logger_level='critical', logger_call_path=call_path, service_code=code, log_message=message))
    def reset_logger_db(self):
        '''重置数据库中的日志表
        Args:
            None
            
        Returns:
            None
        '''
        reset_db()
    
logger = Logger()
