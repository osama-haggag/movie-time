import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.DEBUG)


def make_logger(logger_name):
    logger = logging.getLogger(logger_name)
    return logger
