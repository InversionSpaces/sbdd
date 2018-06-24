from __future__ import absolute_import
from daemon import DaemonContext
from daemon.pidfile import PIDLockFile
from configparser import ConfigParser
from signal import SIGTERM, SIGINT, SIGUSR1

from sbdd.server import SBDServer

class SBDDaemon():
    def reload(self):
        self.config.read(self.config_file)

        server, sbdmsg, api = self.config["SERVER"], self.config["SBDMSG"], self.config["API"]  
	
        addr = (server.get("HOST", fallback="localhost"), 
                server.getint("PORT", fallback=5555))
        msg  = (sbdmsg.get("FMT", fallback="s"), 
                tuple(sbdmsg.get("FIELDS", fallback="Payload").split(",")), 
                sbdmsg.getint("SIZE", fallback=1024))
        api  = (api.get("URL", fallback="http://127.0.0.1/api"), 
                api.get("METHDO", fallback="push"), 
                api.get("JSON_RPC", fallback="2.0"))
        self.server = SBDServer(addr, msg, api)
        
        daemon = self.config["DAEMON"]
	
        pidfile = daemon.get("PIDFILE", fallback="sbdd.pid")
        self.context.pidfile = PIDLockFile(pidfile)
        
        stdout = daemon.get("STDOUT", fallback=None)
        if stdout: self.context.stdout = open(stdout, "w+")
        
        stderr = daemon.get("STDERR", fallback=None)
        if stderr: self.context.stderr = open(stderr, "w+")

    def run(self):
        with self.context:
            self.server.serve_forever()
            
    def down(self):
        self.server.shutdown()
	
    def __init__(self, config_file="sbdd.conf"):      
        self.config_file = config_file        

        self.config = ConfigParser()
        self.context = DaemonContext()
                                     
        self.context.signal_map = {
            SIGINT: self.down,
            SIGUSR1: self.reload
	    }
	    
        self.reload()	

	

	

	
