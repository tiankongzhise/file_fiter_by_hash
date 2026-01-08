from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from ...utils.time_utils import get_current_timestamp, timestamp_to_local_time

class BaseSQLiteModel(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[str] = mapped_column(String, default=get_current_timestamp)
    updated_at: Mapped[str] = mapped_column(String, onupdate=get_current_timestamp,nullable=True)

    @property
    def create_at_local_time(self) -> str | None:
        """创建时间戳转本地时间"""
        return timestamp_to_local_time(self.create_at, ms=True)
    
    @property
    def update_at_local_time(self) -> str | None:
        """更新时间戳转本地时间"""
        return timestamp_to_local_time(self.update_at, ms=True)

    def __repr__(self) -> str:
        # 运行时，动态解析全部字段，以str形式返回
        return f"<{self.__class__.__name__}{','.join([f'{k}={v}' for k,v in self.__dict__.items() if not k.startswith('_')])}>"
