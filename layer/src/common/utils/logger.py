import logging


def get_logger(name):
    '''Sets logger format and level'''
    console_format = logging.Formatter(
        '%(asctime)s~%(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_format)

    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger
