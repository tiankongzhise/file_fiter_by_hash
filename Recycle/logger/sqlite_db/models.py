from sqlalchemy import func,String,Integer,Text
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from ...utils.time_utils import get_current_timestamp,timestamp_to_local_time

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
    logger_call_path: Mapped[str] = mapped_column(String(255))
    service_code: Mapped[str] = mapped_column(String(255))
    log_message: Mapped[str] = mapped_column(Text)
    create_at: Mapped[int] = mapped_column(Integer, default=lambda: get_current_timestamp(ms=True))
    update_at: Mapped[int] = mapped_column(Integer, onupdate=lambda: get_current_timestamp(ms=True), nullable=True)

    @property
    def create_at_local_time(self) -> str | None:
        """创建时间戳转本地时间"""
        return timestamp_to_local_time(self.create_at, ms=True)
    
    @property
    def update_at_local_time(self) -> str | None:
        """更新时间戳转本地时间"""
        return timestamp_to_local_time(self.update_at, ms=True)
    
    def __repr__(self):
        return f"LoggerTable(p_key={self.p_key}, logger_level={self.logger_level}, log_message={self.log_message}, create_at={self.create_at_local_time}, update_at={self.update_at_local_time})"
