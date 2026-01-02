import sys
from pathlib import Path
import random
from sqlalchemy import select


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from database.models import ItemHashResult
from database.save_result import save_item_hash_result
from database.init_db import get_db_engine,reset_db
from database.query_item import query_item_by_hash
from sqlalchemy.orm import Session
import datetime

def create_test_data(data_number: int = 1):
    test_data = []
    for i in range(data_number):
        test_data.append(
            ItemHashResult(
                name=f"test_{i}",
                type=random.choice(["file", "folder"]),
                sha1=f"test_sha1_{i}",
                sha256=f"test_sha256_{i}",
                md5=f"test_md5_{i}",
                size=random.randint(100, 1000000),
                other_hash_info={"test": f"test_{i}"},
            )
        )
    return test_data


def query_item_hash_result():
    engine = get_db_engine()
    with Session(engine) as session:
        stmt = select(ItemHashResult)
        for item in session.scalars(stmt):
            print(item)


def test_item_save():
    print(f'{datetime.datetime.now()}开始测试单个ItemHashResult保存')
    # print(f'{datetime.datetime.now()}开始初始化数据库')
    # reset_db()
    # print(f'{datetime.datetime.now()}数据库初始化完成')
    print(f'{datetime.datetime.now()}开始生成测试数据')
    item_hash_result = create_test_data()[0]
    print(f'{datetime.datetime.now()}生成的测试数据: {item_hash_result}')
    print(f'{datetime.datetime.now()}开始保存测试数据')
    save_item_hash_result(item_hash_result)
    print(f'{datetime.datetime.now()}测试数据保存完成')
    print(f'{datetime.datetime.now()}开始查询测试数据')
    query_item_hash_result()
    print(f'{datetime.datetime.now()}查询测试数据完成')

def test_items_save():
    print(f'{datetime.datetime.now()}开始测试多个ItemHashResult保存')
    # print(f'{datetime.datetime.now()}开始初始化数据库')
    # reset_db()
    # print(f'{datetime.datetime.now()}数据库初始化完成')
    print(f'{datetime.datetime.now()}开始生成测试数据')
    item_hash_result = create_test_data(10)
    print(f'{datetime.datetime.now()}生成的测试数据: {item_hash_result}')
    print(f'{datetime.datetime.now()}开始保存测试数据')
    save_item_hash_result(item_hash_result)
    print(f'{datetime.datetime.now()}测试数据保存完成')
    print(f'{datetime.datetime.now()}开始查询测试数据')
    query_item_hash_result()
    print(f'{datetime.datetime.now()}查询测试数据完成')
    
def test_item_query():
    print(f'{datetime.datetime.now()}开始测试单个ItemHashResult查询')
    print(f'{datetime.datetime.now()}开始查询测试数据')
    item_hash_result = query_item_by_hash(
        sha1="test_sha1_0",
        sha256="test_sha256_0",
        md5="test_md5_0",
    )
    print(f'{datetime.datetime.now()}查询到的测试数据: {item_hash_result}')
    print(f'{datetime.datetime.now()}查询测试数据完成')

if __name__ == "__main__":
    # test_item_save()
    # test_items_save()
    test_item_query()
