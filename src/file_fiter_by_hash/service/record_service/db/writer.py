from .model import RecordServiceModel
from ....core.mysql_core import MySQLEngineManager,MySQLModelManager,MySQLSchemaManager,T
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..logger import logger

class RecordServiceWriter(object):
    def __init__(self):
        self.engine_manager = MySQLEngineManager()
        self.model_manager = MySQLModelManager()
        self.schema_manager = MySQLSchemaManager()
        self.logger = logger
    
    def register(self):
        self.engine_manager.register_engine('record_service')
        self.model_manager.register_model('record_service', RecordServiceModel)
        return self
    def init_schema(self):
        self.schema_manager.init_schema('record_service')
        return self
    
    def add(self, data:T):
        engine = self.engine_manager.get_engine_by_module('record_service')
        with Session(engine) as session:
            try:
                session.add(data)
                result = session.commit()
                self.logger.info(f'record service add success: {data}',extra_info='record_service_add_success')
                return result
            except Exception as e:
                self.logger.error(f'record service add error: {e}',extra_info='record_service_add_error')
            
    
    def update(self, update_item:dict):
        engine = self.engine_manager.get_engine_by_module('record_service')
        table = self.model_manager.get_model('record_service')
        from copy import deepcopy
        temp = deepcopy(update_item)  # Create a copy of the update_item dictionary
        temp_id = temp.pop('id')
        with Session(engine) as session:
            stmt = select(table).where(table.id == temp_id)
            try:
                record = session.scalars(stmt).one()
            except Exception as e:
                self.logger.error(f'record service update error: {e}',extra_info='record_service_update_error_key_error')
            
            try:
                for key, value in temp.items():
                    setattr(record, key, value)
                result = session.commit()
                self.logger.info(f'record service update success: {update_item}',extra_info='record_service_update_success')
            except Exception as e:
                self.logger.error(f'record service update error: {e}',extra_info='record_service_update_error')

            return result

    def delete(self, id:int):
        engine = self.engine_manager.get_engine_by_module('record_service')
        table = self.model_manager.get_model('record_service')
        with Session(engine) as session:
            stmt = select(table).where(table.id == id)
            try:
                record = session.scalars(stmt).one()
            except Exception as e:
                self.logger.error(f'record service delete error: {e}',extra_info='record_service_delete_error_key_error')
            
            try:
                session.delete(record)
                result = session.commit()
                self.logger.info(f'record service delete success: {id}',extra_info='record_service_delete_success')
            except Exception as e:
                self.logger.error(f'record service delete error: {e}',extra_info='record_service_delete_error')
            return result
