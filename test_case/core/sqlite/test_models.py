from file_fiter_by_hash.core.sqlite_core import BaseSQLiteModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String,MetaData



class XTestModel(BaseSQLiteModel):
    metadata = MetaData()
    x: Mapped[str] = mapped_column(String,default="")
    __abstract__ = True


class A(BaseSQLiteModel):
    __tablename__ = "A"
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)

class B(XTestModel):
    __tablename__ = "B"
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)

class C(XTestModel):
    __tablename__ = "C"
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
