from __future__ import absolute_import
import os
from daemon import DaemonContext
from daemon.pidfile import PIDLockFile
from signal import SIGTERM, SIGINT, SIGUSR1
import logging

from sbdd import SBDServer

class SBDDaemon():
    def run(self):
        with self.context:
            logging.info("Daemon up")
            self.context.server.serve_forever()

    def down(self, *args):
        logging.info("Daemon down")
        self.context.server.shutdown()
        
    def setPIDFile(self, pidfile):
        self.context.pidfile = PIDLockFile(pidfile)
        
    def setSTDOut(self, stdout):
        if self.context.stdout: self.context.stdout.close()
        self.context.stdout = open(stdout, "w+")
        
    def setSTDErr(self, stderr):
        if self.context.stderr: self.context.stderr.close()
        self.context.stderr = open(stderr, "w+")

    def __init__(self, addr):
        self.context = DaemonContext()

        self.context.server = SBDServer(addr)
        self.context.files_preserve = [self.context.server.fileno()]
        self.context.signal_map = {
            SIGINT: self.down
        }

        

