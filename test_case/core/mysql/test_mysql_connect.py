from file_fiter_by_hash.core.mysql_core.engine_manager import MySQLEngineManager


def test_engine_get():
    engine = MySQLEngineManager().get_engine_by_db("test_db")
    print(engine)


if __name__ == "__main__":
    test_engine_get()
