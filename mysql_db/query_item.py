from sqlalchemy.orm import Session
from sqlalchemy import text, select
from .init_db import get_db_engine
from .models import ItemHashResult


def query_item_by_hash(sha1: str, sha256: str, md5: str):
    """根据文件哈希结果查询数据库"""
    engine = get_db_engine()
    with Session(engine) as session:
        stmt = (
            select(ItemHashResult)
            .where(ItemHashResult.sha1 == sha1)
            .where(ItemHashResult.sha256 == sha256)
            .where(ItemHashResult.md5 == md5)
        )
        result = session.scalars(stmt).one()
        return result
