from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from .init_db import get_db_engine
from .models import ItemHashResult, SpecialFolderTable, TempHashTable
from ..logger import get_logger

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
            if result is None:
                return False
            else:
                return True
    except Exception as e:
        logger.error(f"根据文件哈希结果查询数据库失败: {e}")
        return None


def query_item_by_special_folder_name(name: str):
    """根据特殊文件夹名称查询数据库"""
    engine = get_db_engine()
    try:
        with Session(engine) as session:
            stmt = (
                select(SpecialFolderTable)
                .where(SpecialFolderTable.name == name)
            )
            result = session.scalars(stmt).one_or_none()
            if result is None:
                return False
            return result
    except Exception as e:
        logger.error(f"根据特殊文件夹名称查询数据库失败: {e}")
        return None


def get_all_special_folder():
    """获取所有特殊文件夹名称和大小"""
    engine = get_db_engine()
    try:
        with Session(engine) as session:
            stmt = select(SpecialFolderTable.name, SpecialFolderTable.size)
            result = session.scalars(stmt).all()
            return result
    except Exception as e:
        logger.error(f"获取所有特殊文件夹名称和大小失败: {e}")
        return None


def is_temp_hash_table(hash_tag: str = None, name: str = None, size: int = None):
    """判断哈希标签是否在临时哈希表中"""
    engine = get_db_engine()
    try:
        with Session(engine) as session:
            if hash_tag is None:
                stmt = (
                    select(TempHashTable)
                    .where(TempHashTable.name == name)
                    .where(TempHashTable.size == size)
                )
            else:
                stmt = (
                    select(TempHashTable)
                    .where(TempHashTable.hash_tag == hash_tag)
                )
            result = session.scalars(stmt).one_or_none()
            if result is None:
                return False
            return True
    except Exception as e:
        logger.error(f"判断哈希标签是否在临时哈希表中失败: {e}")
        return None


def insert_item_hash_result(item_hash_result: ItemHashResult):
    """插入哈希结果"""
    engine = get_db_engine()
    try:
        with Session(engine) as session:
            session.add(item_hash_result)
            session.commit()
            return True
    except Exception as e:
        logger.error(f"插入哈希结果失败: {e}")
        return False


def insert_special_folder(special_folder: SpecialFolderTable):
    """插入特殊文件夹"""
    engine = get_db_engine()
    try:
        with Session(engine) as session:
            session.add(special_folder)
            session.commit()
            return True
    except Exception as e:
        logger.error(f"插入特殊文件夹失败: {e}")
        return False


def insert_temp_hash(temp_hash: TempHashTable):
    """插入临时哈希"""
    engine = get_db_engine()
    try:
        with Session(engine) as session:
            session.add(temp_hash)
            session.commit()
            return True
    except Exception as e:
        logger.error(f"插入临时哈希失败: {e}")
        return False
