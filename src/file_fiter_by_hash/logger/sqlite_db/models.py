from sqlalchemy import func,String,Integer
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from datetime import datetime
class Base(DeclarativeBase):
    pass
class LoggerTable(Base):
    '''
    日志表
    args:
        log_type: 日志类型
        log_message: 日志消息
    '''
    __tablename__ = "logger_table"
    p_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    logger_level: Mapped[str] = mapped_column(String(10))
    log_message: Mapped[str] = mapped_column(String(255))
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"LoggerTable(p_key={self.p_key}, logger_level={self.logger_level}, log_message={self.log_message}, create_at={self.create_at}, update_at={self.update_at})"
