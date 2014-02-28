import logging

from singleton import Singleton

class Logger(object):
    __metaclass__ = Singleton

    def __init__(self, name):
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)

        console_lh = logging.StreamHandler()
        console_lh.setFormatter(
            logging.Formatter("%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(message)s"))
        console_lh.setLevel(logging.DEBUG)
        self.log.addHandler(console_lh)
        self.log.setLevel(logging.DEBUG)

    def get_log(self):
        return self.log;

