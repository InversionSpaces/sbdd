from __future__ import absolute_import
from daemon import DaemonContext
from lockfile import FileLock
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
	
        pidfile = daemon.get("PIDFILE", fallback="/var/run/sbdd.pid")
        self.context.pidfile = FileLock(pidfile)

    def run(self):
        with self.context:
            self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
	
    def __init__(self,	stdin=None, stdout=None, stderr=None,
		config_file="sbdd.conf"):
        self.config_file = config_file        

        self.config = ConfigParser()
        self.context = DaemonContext()

        self.reload()	

        self.context.signal_map = {
            SIGTERM: self.stop,
            SIGINT: self.stop,
            SIGUSR1: self.reload
	    }

	

	

	
