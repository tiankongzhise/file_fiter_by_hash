from .logger import logger
from .schmeas import ClassifySuccessSchema
from .db import RecordServiceWriter, ProcessRecord


class Recorder:
    def __init__(self, db_path: str):
        self.db_writer = RecordServiceWriter().register().init_schema()
        self.

    def add_record(self, record: ClassifySuccessSchema):
