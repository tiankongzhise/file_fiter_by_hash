from file_fiter_by_hash.logger import create_logger
from file_fiter_by_hash.core.sqlite_core import SQLiteEngineManager,SQLiteSchemaManager
from sqlalchemy.orm import Session
from file_fiter_by_hash.logger.db.model import LoggerRecord
from sqlalchemy import engine, select


def simple_test():
    # test_new_logger = create_logger("test_new_logger", "test_service")
    # test_new_logger.info("This is a test log message.")
    # test_new_logger.warning("This is a test log message.")
    # test_new_logger.error("This is a test log message.")
    # test_new_logger.critical("This is a test log message.")
    # test_new_logger.debug("This is a test log message.")
    manager = SQLiteEngineManager()
    engine = manager.get_engine_by_db('logger')

    print('\n 数据库查询结果 \n')
    with Session(engine) as session:
        stmt = select(LoggerRecord).order_by(LoggerRecord.id.asc())
        result = session.scalars(stmt).all()
        for row in result:
            print(row)
    # schema_manager = SQLiteSchemaManager()
    # schema_manager.reset_schema('logger')
if __name__ == "__main__":
    simple_test()
