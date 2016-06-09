import logging
import sys


def get_logger(name):
    """Gets a formatted logger."""
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(log_format)
    log.addHandler(ch)
    return log
