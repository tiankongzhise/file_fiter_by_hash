from modulefinder import test
from file_fiter_by_hash.logger import logger,query_logger

def test_reset_db():
    logger.reset_logger_db()
    logger_info = query_logger()
    assert len(logger_info) == 0

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
def test_query_warning():
    logger_info = query_logger(logger_level=['warning','error','critical'])
    for log in logger_info:
        print(log)
    
if __name__ == '__main__':
    # print(f'-*50 test_reset_db -*50')
    # test_reset_db()
    # print(f'-*50 test_logger -*50')
    # test_logger()
    # print(f'-*50 test_set_logger_level -*50')
    # test_set_logger_level()
    # print(f'-*50 test_set_logger_attr -*50')
    # test_set_logger_attr()
    # print(f'-*50 test_false_console_print -*50')
    # test_false_console_print()
    # print(f'-*50 test_false_persistence -*50')
    # test_false_persistence()
    # print(f'-*50 test_query_logger_model -*50')
    # logger.set_logger_config(is_call_path=True)
    # logger.set_logger_config(is_persistence=True)
    # logger.set_logger_config(is_print_console=True)
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warning message')
    # logger.error('error message')
    # logger.critical('critical message')
    # print(f'-*50 test_query_logger_db -*50')
    # test_query_logger_db()
    test_query_warning()
