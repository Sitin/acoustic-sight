import logging
import os
import time


ACOUSTIC_SIGHT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(ACOUSTIC_SIGHT_DIR)
ACOUSTIC_SIGHT_SERVER_DIR = os.path.join(PROJECT_DIR, 'acoustic_sight_server')
SERVICES_DIR = os.path.join(PROJECT_DIR, 'services')
DATA_DIR = os.path.join(SERVICES_DIR, 'data')


def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger


class TimeMeasurer(object):
    def __init__(self, logger=None, level=logging.DEBUG):
        self.logger = logger
        self.level = level

    def measure_time(self, msg, fn, *args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()

        log_text = '{msg} in {milis:08.6f} ms'.format(msg=msg, milis=(end - start) * 1000)
        if self.logger is None:
            print(log_text)
        else:
            print(log_text)
            self.logger.log(self.level, log_text)

        return result

    def decorate(self, fn, msg='Operation'):
        def decorated(*args, **kwargs):
            return self.measure_time(msg, fn, *args, **kwargs)

        return decorated

    def decorate_method(self, obj, fn, msg='Operation'):
        fn_name = fn.__name__
        setattr(obj, fn_name, self.decorate(fn, msg=msg))

