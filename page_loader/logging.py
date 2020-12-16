import logging


def get_logging():
    return logging.basicConfig(level=logging.INFO,
                               format='%(levelname)s: %(message)s')
