from configparser import RawConfigParser

from sbdd import SBDServer
from sbdd import SBDDaemon


def getConfig(conffile, config):
    if conffile:
        config = RawConfigParser()
        config.read(conffile)
    elif not config: 
        raise ValueError("No source given")
    return config
    

def getServerConfig(config):
    server, sbdmsg, jsonapi = config["SERVER"], config["SBDMSG"], config["API"]
    
    addr = (server.get("HOST", fallback="localhost"), 
            server.getint("PORT", fallback=5555))
    msg  = (sbdmsg.get("FMT", fallback="s"), 
            tuple(sbdmsg.get("FIELDS", fallback="Payload").split(",")), 
            sbdmsg.getint("SIZE", fallback=1024))
    api  = (jsonapi.get("URL", fallback="http://127.0.0.1/api"), 
            jsonapi.get("METHOD", fallback="pushdata"), 
            jsonapi.get("JSON_RPC", fallback="2.0"))
            
    return (addr, msg, api)
    

def getDaemonConfig(config):
    daemon = config["DAEMON"]
        
    pidfile = daemon.get("PIDFILE", fallback="sbdd.pid")
    stdout  = daemon.get("STDOUT", fallback="/dev/null")
    stderr  = daemon.get("STDERR", fallback="/dev/null")
    
    return (pidfile, stdout, stderr)
    

def SBDServerFromConfig(conffile=None, config=None):
    config = getConfig(conffile, config)
    
    return SBDServer(getServerConfig(config))
    
    
def SBDDaemonFromConfig(conffile=None, config=None):
    config = getConfig(conffile, config)
             
    return SBDDaemon(getServerConfig(config), getDaemonConfig(config))
    
