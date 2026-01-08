from file_fiter_by_hash.core.sqlite_core import SQLiteEngineManager,SQLiteModelManager,SQLiteSchemaManager
from test_models import XTestModel
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect

def test_manager():
    engine_manager = SQLiteEngineManager()
    model_manager = SQLiteModelManager()
    schema_manager = SQLiteSchemaManager()
    engine_manager.register_engine('test_module','test_db')
    model_manager.register_model('test_module', XTestModel)
    schema_manager.init_schema('test_module')
    engine = engine_manager.get_engine_by_module('test_module')
    inspector = inspect(engine)
    columns = inspector.get_columns('C')
    for column in columns:
        print(f'{column["name"]}: {column["type"]}')

def test_a_live():
    schema_manager = SQLiteSchemaManager()
    print(schema_manager.engine_manager.engine)
    print(schema_manager.model_manager.models)


if __name__ == '__main__':
    test_manager()
    test_a_live()
