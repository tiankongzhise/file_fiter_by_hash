from sqlalchemy.orm import Session
from ...schmeas import LoggerInfo
from .init_db import get_db_engine
from .models import LoggerTable

def sql_logger_write(logger_info:LoggerInfo):
    db_engile = get_db_engine()
    with Session(db_engile) as session:
        logger_table = LoggerTable(
            logger_level=logger_info.logger_level,
            log_message=logger_info.log_message
        )
        session.add(logger_table)
        session.commit()
