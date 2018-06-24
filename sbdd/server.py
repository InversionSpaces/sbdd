import socketserver
import json
import requests

from sbdd.handler import SBDHandle


class SBDServer(socketserver.TCPServer):
    allow_reuse_address = True
    
    def __init__(self, addr, msg, api):
        super().__init__(addr, SBDHandler)
        
        self.fmt, self.fields, self.size = msg
        self.url, self.method, self.ver  = api
        self.reqnum = 0
        

class SBDHandler(socketserver.BaseRequestHandler):
    def handle(self):
        payload = (self.server.fields, self.server.fmt)
        
        self.data = self.request.recv(self.server.size)
        self.data = SBDHandle(self.data, payload)
        
        headers = {"content-type": "application/json"}
        payload = {
            "method": self.server.method,
            "params": self.data,
            "jsonrpc": self.server.ver,
            "id": self.server.reqnum,
        }
        response = requests.post(self.server.url, data=json.dumps(payload), headers=headers).json()
        
        self.server.reqnum += 1
        

