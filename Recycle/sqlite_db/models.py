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

class SpecialFolderTable(Base):
    '''
    特殊文件夹列表
    args:
        name: 特殊文件夹名称
        size: 特殊文件夹大小
    '''
    __tablename__ = "special_folder_table"
    p_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    size: Mapped[int] = mapped_column(Integer)
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_onupdate=func.now(), nullable=True)

class FileOperationRecordTable(Base):
    '''
    文件操作记录
    args:
        operation_type: 操作类型
        file_path: 文件路径
        file_hash: 文件哈希值
    '''
    __tablename__ = "file_operation_record"
    p_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    operation: Mapped[str] = mapped_column(String(10))
    source_path: Mapped[str] = mapped_column(String(255))
    target_path: Mapped[str] = mapped_column(String(255))
    file_name: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(10))
    hash_info: Mapped[dict] = mapped_column(JSON)
    operation_status: Mapped[str] = mapped_column(String(10))
    error_message: Mapped[str] = mapped_column(String(255), default='')
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_onupdate=func.now(), nullable=True)

class TempHashTable(Base):
    '''
    临时哈希表
    args:
        hash_tag: 哈希标签
        type: 文件类型
        size: 文件大小
    '''
    __tablename__ = "temp_hash_table"
    p_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hash_tag: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(10))
    size: Mapped[int] = mapped_column(Integer)
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_onupdate=func.now(), nullable=True)
