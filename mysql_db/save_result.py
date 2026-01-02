from sqlalchemy.orm import Session
from sqlalchemy import text
from .init_db import get_db_engine 
from .models import ItemHashResult


def save_item_hash_result(item_hash_result: ItemHashResult|list[ItemHashResult]):
    """保存文件哈希结果到数据库"""
    engine = get_db_engine()
    with Session(engine) as session:
        match item_hash_result:
            case ItemHashResult():
                session.add(item_hash_result)
            case list():
                session.add_all(item_hash_result)
        session.commit()
