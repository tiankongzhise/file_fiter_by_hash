from sqlmodel import Session
from .init_db import get_db_engine as get_db

def test_connect():
    print('test_connect')
    
    engine = get_db()
    with Session(engine) as session:
        query_sql = 'SELECT VERSION()'
        result = session.exec(query_sql).first()
        print(result)


def test_table_exists():
    print('test_table_exists')
    engine = get_db()
    with Session(engine) as session:
        query_sql = 'SELECT to_regclass(\'file_hash_result\')'
        result = session.exec(query_sql).first()
        print(result)
