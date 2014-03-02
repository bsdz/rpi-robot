import logging

from singleton import Singleton

class Logger(object):
    __metaclass__ = Singleton

    def __init__(self, name):
        self.log = logging.getLogger(name)

        console_lh = logging.StreamHandler()
        console_lh.setFormatter(
            logging.Formatter("%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(name)s|%(funcName)s|%(message)s"))
        console_lh.setLevel(logging.DEBUG)
        self.log.addHandler(console_lh)

        file_lh = logging.FileHandler("./robot.log")
        file_lh.setFormatter(
            logging.Formatter("%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(name)s|%(funcName)s|%(message)s"))
        file_lh.setLevel(logging.DEBUG)
        self.log.addHandler(file_lh)

        self.log.setLevel(logging.DEBUG)

    def get_log(self):
        return self.log;

