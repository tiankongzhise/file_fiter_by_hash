from .logger import create_logger
from .logger.logger import Logger

# 全局 logger 实例缓存
_logger_cache = {}


def get_logger(name: str = "default") -> Logger:
    """获取或创建 logger 实例"""
    if name not in _logger_cache:
        _logger_cache[name] = create_logger(name, "default")
    return _logger_cache[name]


__all__ = [
    "create_logger",
    "get_logger"
]
