'''
Created on 3 Oct 2017

@author: blair
'''
import subprocess

from robot.utility.logger import Logger
log = Logger("Process").get_log()

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
