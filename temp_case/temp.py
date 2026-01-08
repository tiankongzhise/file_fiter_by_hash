from modulefinder import test
from sqlalchemy import create_engine,text
from sqlalchemy.orm import DeclarativeBase,Session
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import MetaData, String 

class Base(DeclarativeBase):
    pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}()>"


class A(Base):
    metadata = MetaData()
    id: Mapped[int] = mapped_column(primary_key=True)
    a: Mapped[str] = mapped_column(String(50))

    __abstract__ = True

class B(Base):
    metadata = MetaData()
    id: Mapped[int] = mapped_column(primary_key=True)
    b: Mapped[str] = mapped_column(String(50))
    __abstract__ = True

class C(A):
    __tablename__ = "c"
    c: Mapped[str] = mapped_column(String(50))

class D(B):
    __tablename__ = "d"
    d: Mapped[str] = mapped_column(String(50))

class E(A):
    __tablename__ = "e"
    e: Mapped[str] = mapped_column(String(50))

class F(B):
    __tablename__ = "f"
    f: Mapped[str] = mapped_column(String(50))

def create_all():
    engine = create_engine("sqlite:///example.db")
    Base.metadata.create_all(engine)
def create_a_all():
    engine = create_engine("sqlite:///example.db")
    A.metadata.create_all(engine)
def create_b_all():
    engine = create_engine("sqlite:///example.db")
    B.metadata.create_all(engine)

def test_query():
    engine = create_engine("sqlite:///example.db")
    with Session(engine) as session:
        # 查询出全部已经存在的表名称
        tables = session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).scalars().all()
        for table in tables:
            print(table)
def drop_all():
    engine = create_engine("sqlite:///example.db")
    Base.metadata.drop_all(engine)
def drop_a_all():
    engine = create_engine("sqlite:///example.db")
    A.metadata.drop_all(engine)
def drop_b_all():
    engine = create_engine("sqlite:///example.db")
    B.metadata.drop_all(engine)
if __name__ == "__main__":
    print("create_all")  # 创建所有表
    create_all()
    print('创建所有表结果')
    test_query()
    print("create_a_all")  # 创建a所有表
    create_a_all()
    print('创建a所有表结果')
    test_query()
    print("drop_a_all")  # 删除a所有表
    drop_a_all()
    print('删除a所有表结果')
    test_query()
    print("create_b_all")  # 创建b所有表
    create_b_all()
    print('创建b所有表结果')
    test_query()
    print('删除b所有表结果')
    drop_b_all()
    print("drop_b_all")  # 删除b所有表
    test_query()
