from ...core.sqlite_core import BaseSQLiteModel
from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  String, Text, Index


class LoggerModelBase(BaseSQLiteModel):
    __abstract__ = True
    metadata = MetaData()


class LoggerRecord(LoggerModelBase):
    __tablename__ = "logger_record"
    logger_name: Mapped[str] = mapped_column(String(50))
    logger_level: Mapped[str] = mapped_column(String(10))
    logger_message: Mapped[str] = mapped_column(Text)
    service: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))
    extra_info: Mapped[str] = mapped_column(Text)
    call_info: Mapped[str] = mapped_column(Text)

__table_args__ = (
    Index("idx_level", "logger_level"),
    Index("idx_service_status_extra_info", "service", "status", "extra_info"),
)
