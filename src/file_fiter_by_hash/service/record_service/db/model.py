from ....core.mysql_core import BaseMySQLModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String,JSON,Text,Integer,UniqueConstraint,Boolean
from sqlalchemy import MetaData

class RecordServiceModel(BaseMySQLModel):
    metadata = MetaData()
    __abstract__ = True

    version: Mapped[int] = mapped_column(Integer, default=1)

    __mapper_args__ = {
        'version_id_col': version,
    }


class ProcessRecord(RecordServiceModel):
    __tablename__ = 'process_record'
    item_name: Mapped[str] = mapped_column(String(255))
    source_path: Mapped[str] = mapped_column(Text)
    item_type: Mapped[str] = mapped_column(String(10))
    item_size: Mapped[int] = mapped_column(Integer)
    md5: Mapped[str] = mapped_column(String(32))
    sha1: Mapped[str] = mapped_column(String(40))
    sha256: Mapped[str] = mapped_column(String(64))
    other_hash_info: Mapped[dict] = mapped_column(JSON, nullable=True)
    classify_result: Mapped[str] = mapped_column(String(10))
    process_status: Mapped[str] = mapped_column(String(32))
    process_result: Mapped[str] = mapped_column(String(10))
    zipped_path: Mapped[str] = mapped_column(Text, nullable=True)
    zipped_size: Mapped[int] = mapped_column(Integer)
    zipped_md5: Mapped[str] = mapped_column(String(32))
    zipped_sha1: Mapped[str] = mapped_column(String(40))
    zipped_sha256: Mapped[str] = mapped_column(String(64))
    other_unzip_info: Mapped[dict] = mapped_column(JSON, nullable=True)
    unzip_path: Mapped[str] = mapped_column(Text, nullable=True)
    unzip_size: Mapped[int] = mapped_column(Integer, nullable=True)
    unzip_md5: Mapped[str] = mapped_column(String(32), nullable=True)
    unzip_sha1: Mapped[str] = mapped_column(String(40), nullable=True)
    unzip_sha256: Mapped[str] = mapped_column(String(64), nullable=True)
    other_unzip_info: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_compiled: Mapped[bool] = mapped_column(Boolean, default=False)
    fail_reason: Mapped[dict] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        UniqueConstraint('source_path', name='uix_source_path'),
    )
