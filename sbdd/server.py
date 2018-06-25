import socketserver
import json
import requests
import logging

from sbdd import SBDHandle


class SBDServer(socketserver.TCPServer):
    allow_reuse_address = True
    
    def __init__(self, addr, msg, api):
        super().__init__(addr, SBDHandler)
        
        self.fmt, self.fields, self.size = msg
        self.url, self.method, self.ver  = api
        self.reqnum = 0
        

class SBDHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Handling request")
        payload = (self.server.fields, self.server.fmt)
        
        try:
            self.data = self.request.recv(self.server.size)
            self.data = SBDHandle(self.data, payload)
        except Exception as e:
            logging.error(e)
            return
        else:
            logging.info(self.data)
        
        headers = {"content-type": "application/json"}
        payload = {
            "method": self.server.method,
            "params": self.data,
            "jsonrpc": self.server.ver,
            "id": self.server.reqnum,
        }
        try:
            response = requests.post(self.server.url, data=json.dumps(payload), headers=headers).json()
        except Exception as e:
            logging.error(e)
            return
        else:
            logging.info(response)
        
        self.server.reqnum += 1
        

