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
	
    def __init__(self, server, daemon):
        self.context = DaemonContext(working_directory=os.getcwd())
        
        self.context.server = SBDServer(*server)
        self.context.files_preserve = [self.context.server.fileno()]
        
        pidfile, stdout, stderr = daemon
        if pidfile: self.context.pidfile = PIDLockFile(pidfile)
        if stdout: self.context.stdout = open(stdout, "w+")
        if stderr: self.context.stderr = open(stderr, "w+")
        
        self.context.signal_map = {
            SIGINT: self.down
	    }	

	

	

	
