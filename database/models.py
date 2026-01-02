from sqlmodel import Field, SQLModel,UniqueConstraint
from datetime import datetime
from sqlmodel import Column,DATETIME,func


class FileHashResult(SQLModel, table=True):
    p_key: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: str
    size: int
    sha1:str
    sha256:str
    md5:str
    create_at:datetime = Field(default_factory=datetime.now)
    update_at:datetime = Column( server_default=None,server_onupdate=func.now)
    
    __table_args__ = (
        UniqueConstraint("sha1","sha256","md5",name="uq_hash_value"),
    )
