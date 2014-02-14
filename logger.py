import logging

log = logging.getLogger("Main")
log.setLevel(logging.DEBUG)

console_logHandler = logging.StreamHandler()
console_logHandler.setFormatter(
    logging.Formatter("%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(message)s"))
console_logHandler.setLevel(logging.DEBUG)
log.addHandler(console_logHandler)
log.setLevel(logging.DEBUG)

class Logger(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

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

