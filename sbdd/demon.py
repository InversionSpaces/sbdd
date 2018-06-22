from daemon import DaemonContext
from lockfile import FileLock
from configparser import ConfigParser
from signal import SIGTERM, SIGINT, SIGUSR1

from server import SBDServer

class SBDDaemon():
    def reload(self):
        self.config.read(self.config_file)
	
        addr = (self.config["SERVER"]["HOST"], int(self.config["SERVER"]["PORT"]))
        msg = (self.config["SBDMSG"]["FMT"], self.config["SBDMSG"]["FIELDS"], self.config["SBDMSG"]["SIZE"])
        api = (self.config["API"]["URL"], self.config["API"]["METHOD"], self.config["API"]["JSON_RPC"])
        self.server = SBDServer(addr, msg, api)
	
        pidfile = self.config["DAEMON"]["PIDFILE"]
        self.context.pidfile = FileLock(pidfile)

    def run(self):
        with self.context:
            self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
	
    def __init__(self,	stdin=None, stdout=None, stderr=None,
			config_file="/etc/sbdd.conf"):
        self.config_file = config_file        

        self.config = ConfigParser()
        self.context = DaemonContext()

        self.reload()	

        self.context.signal_map = {
            SIGTERM: self.stop,
            SIGINT: self.stop,
            SIGUSR1: self.reload
	}

	

	

	
