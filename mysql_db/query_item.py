from sqlalchemy.orm import Session
from sqlalchemy import text, select
from .init_db import get_db_engine
from .models import ItemHashResult
from logger import get_logger

logger = get_logger()


def query_item_by_hash(sha1: str, sha256: str, md5: str):
    """根据文件哈希结果查询数据库"""
    engine = get_db_engine()
    try:
        with Session(engine) as session:
            stmt = (
                select(ItemHashResult)
                .where(ItemHashResult.sha1 == sha1)
                .where(ItemHashResult.sha256 == sha256)
                .where(ItemHashResult.md5 == md5)
            )
            result = session.scalars(stmt).one_or_none()
            print(result)
            if result is None:
                return False
            else:
                return True
    except Exception as e:
        logger.error(f"根据文件哈希结果查询数据库失败: {e}")
        return None
