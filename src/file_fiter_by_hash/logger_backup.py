import logging
import datetime
import pathlib

class Logger:
    _singleton = None
    
    def __new__(cls, name: str = __name__):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton
    
    def __init__(self,name:str = __name__):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        self.create_logger_file()
        self._singleton = self

    def create_logger_file(self,file_dir:str = None):
        if not file_dir:
            file_dir = pathlib.Path(__file__).parent / "logs"
        file_dir.mkdir(parents=True, exist_ok=True)
        log_path = file_dir / f"{self.logger.name}_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        log_path_str = str(log_path.resolve())

        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler) and getattr(handler, "baseFilename", None) == log_path_str:
                return

        self.logger_file = logging.FileHandler(log_path_str, encoding='utf-8')
        self.logger_file.setFormatter(self.formatter)
        self.logger.addHandler(self.logger_file)

    def get_logger(self):
        return self.logger


def get_logger() -> logging.Logger:
    return Logger('file_filter_by_hash').get_logger()
