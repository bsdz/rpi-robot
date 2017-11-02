'''subprocess helpers

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import subprocess
import logging

log = logging.getLogger(f'process')

class CommandResults(object):
    def __init__(self, out, err, retcode):
        self.out = out
        self.err = err
        self.retcode = retcode

def execute_command(command_args):
    sp = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    if out:
        log.info("standard output of subprocess:\n%s" % out)

    if err:
        log.info("standard error of subprocess:\n%s" % err)

    return CommandResults(out, err, sp.returncode)
