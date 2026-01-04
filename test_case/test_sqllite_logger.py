from file_fiter_by_hash.logger import logger,query_logger


def test_logger():
    logger.debug('test_logger debug message')
    logger.info('test_logger info message')
    logger.warning('test_logger warning message')
    logger.error('test_logger error message')
    logger.critical('test_logger critical message')


def test_set_logger_level():
    logger.set_logger_config(console_logger_level='warning')
    logger.debug('test_set_logger_level debug message')
    logger.info('test_set_logger_level info message')
    logger.warning('test_set_logger_level warning message')
    logger.error('test_set_logger_level error message')
    logger.critical('test_set_logger_level critical message')

def test_set_logger_attr():
    logger.set_logger_config(console_logger_level='Debug')
    logger.set_logger_config(is_call_path=False)
    logger.debug('test_set_logger_attr debug message')
    logger.info('test_set_logger_attr info message')
    logger.warning('test_set_logger_attr warning message')
    logger.error('test_set_logger_attr error message')
    logger.critical('test_set_logger_attr critical message')

def test_false_console_print():
    logger.set_logger_config(is_print_console=False)
    logger.debug('test_false_console_print debug message')
    logger.info('test_false_console_print info message')
    logger.warning('test_false_console_print warning message')
    logger.error('test_false_console_print error message')
    logger.critical('test_false_console_print critical message')

def test_false_persistence():
    logger.set_logger_config(is_persistence=False)
    logger.set_logger_config(is_print_console=True)
    logger.debug('test_false_persistence debug message')
    logger.info('test_false_persistence info message')
    logger.warning('test_false_persistence warning message')
    logger.error('test_false_persistence error message')
    logger.critical('test_false_persistence critical message')

def test_query_logger_db():
    logger_info = query_logger()
    for log in logger_info:
        print(log)
    
    
if __name__ == '__main__':
    test_logger()
    test_set_logger_level()
    test_set_logger_attr()
    logger.set_logger_config(is_call_path=True)
    logger.set_logger_config(is_persistence=True)
    logger.set_logger_config(is_print_console=True)
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
    test_query_logger_db()
