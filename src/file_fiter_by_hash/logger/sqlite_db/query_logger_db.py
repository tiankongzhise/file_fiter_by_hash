from sqlalchemy.orm import Session
from sqlalchemy import select
from .init_db import get_db_engine
from .models import LoggerTable

def query_logger(logger_time:str|None=None,logger_level:str|list[str]|None=None,logger_message:str|None=None):
    db_engile = get_db_engine()
    with Session(db_engile) as session:
        stmt = select(LoggerTable)
        if logger_time is None and logger_level is None and logger_message is None:
            stmt = stmt.order_by(LoggerTable.create_at.desc())
            result = session.scalars(stmt).all()
            return result
        if logger_time:
            stmt = stmt.where(LoggerTable.create_at >= logger_time)
        if logger_level:
            if isinstance(logger_level,str):
                logger_level = [logger_level]
            stmt = stmt.where(LoggerTable.logger_level.in_(logger_level))
        if logger_message:
            stmt = stmt.where(LoggerTable.log_message.like(f'%{logger_message}%'))
        result = session.scalars(stmt).all()
        return result
