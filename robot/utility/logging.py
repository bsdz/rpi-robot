'''logging

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''

import logging

import robot.settings as settings

console_log_handler = logging.StreamHandler()
console_log_handler.setFormatter(
    logging.Formatter("%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(name)s|%(funcName)s|%(message)s"))
console_log_handler.setLevel(logging.DEBUG)

file_log_handler = logging.FileHandler(settings.log_file)
file_log_handler.setFormatter(
    logging.Formatter("%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(name)s|%(funcName)s|%(message)s"))
file_log_handler.setLevel(logging.DEBUG)

