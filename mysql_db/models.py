from sqlalchemy import func,String,Integer,UniqueConstraint
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from sqlalchemy import JSON
from datetime import datetime

class Base(DeclarativeBase):
    pass

class ItemHashResult(Base):
    '''
    项目文件哈希结果表
    args:
        name: 项目文件名称
        type: 项目文件类型
        size: 项目文件大小
        sha1: 项目文件sha1哈希值
        sha256: 项目文件sha256哈希值
        md5: 项目文件md5哈希值
        other_hash_info: 其他哈希信息
    '''
    
    __tablename__ = "item_hash_result"
    
    p_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    type: Mapped[str] = mapped_column(String(10))
    size: Mapped[int] = mapped_column(Integer)
    sha1: Mapped[str] = mapped_column(String(40))
    sha256: Mapped[str] = mapped_column(String(64))
    md5: Mapped[str] = mapped_column(String(32))
    other_hash_info:Mapped[dict] = mapped_column(JSON)
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_onupdate=func.now(), nullable=True)
    
    __table_args__ = (
        UniqueConstraint("sha1","sha256","md5",name="uq_hash_value"),
    )

    def __repr__(self):
        return f"ItemHashResult({self.name}, {self.type}, {self.size}, {self.sha1}, {self.sha256}, {self.md5}, {self.other_hash_info})"
