from .logger import Logger


def create_logger(
    logger_name: str,
    service_name: str,
    status_map: dict | None = None,
    extra_info_map: dict | None = None,
) -> Logger:
    logger = Logger(logger_name)
    logger.set_service(service_name)
    logger.set_status_map(status_map)
    logger.set_extra_info_map(extra_info_map)
    return logger

__all__ = [
    "create_logger"
]
