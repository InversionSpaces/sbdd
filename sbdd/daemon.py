from daemon import DaemonContext
from locckfile import FileLock
from configparser import ConfigParser
from signal import SIGTERM, SIGINT, SIGUSR1

class SBDDaemon():
    def reload(self):
	config.read(config_file);
	
	addr = (config["SERVER"]["HOST"], config["SERVER"]["PORT"])
	msg = (config["SBDMSG"]["FMT"], config["SBDMSG"]["FIELDS"], config["SBDMSG"]["SIZE"])
	api = (config["API"]["URL"], config["API"]["METHOD"], config["API"]["JSON_RPC"])
	self.server = SBDServer(addr, msg, api)
	
	pidfile = config["DAEMON"]["PIDFILE"]
	self.context.pidfile = FileLock(pidfile)

    def run(self):
	with self.context:
		self.server.serve_forever()

    def stop(self):
	self.server.shutdown()
	
    def __init__(self,	stdin=None, stdout=None, stderr=None,
			config_file="/etc/sbdd.conf"):
	self.config = ConfigParser()
	self.context = DaemonContext()

	self.reload()	

	self.context.signal_map = {
		SIGTERM: self.stop,
		SIGINT: self.stop,
		SEGUSR1: self.reload
	}

	

	

	
