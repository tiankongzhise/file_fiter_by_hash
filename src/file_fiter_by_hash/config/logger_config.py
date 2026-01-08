from dataclasses import dataclass
@dataclass
class LoggerConfig:
    '''日志配置
    args:
        is_print_console: 是否打印到控制台
        is_persistence: 是否持久化到数据库
        is_call_path: 是否记录调用路径
        console_logger_level: 控制台日志输出级别
        persistence_logger_level: 数据库日志记录级别
    '''
    is_print_console = True
    is_persistence  = True
    console_logger_level = 'debug'
    persistence_logger_level = 'info'
    logger_level_map = {
        'debug': 10,
        'info': 20,
        'warning': 30,
        'error': 40,
        'critical': 50,
    }
    logger_status = ['success', 'fail']
