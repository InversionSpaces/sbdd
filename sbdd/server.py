import socketserver
import json
import requests
import logging

from sbdd import SBDHandle


class SBDServer(socketserver.TCPServer):
    allow_reuse_address = True
    
    def __init__(self, addr):
        super().__init__(addr, SBDHandler)
        
        self.api = list()
        self.payload = None 
        self.msgsize = 4096
        self.reqnum = 0
    
    def setMsgSize(self, msgsize):
        self.msgsize = msgsize
     
    def addApi(self, api):
        self.api.append(api)
    
    def setPayload(self, payload):
        self.payload = payload
        
        

class SBDHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Handling request {}".format(self.server.reqnum))
        
        try:
            logging.info("Getting data")
            self.data = self.request.recv(self.server.msgsize)
            logging.debug(self.data)
            
            logging.info("Parcing data")
            self.data = SBDHandle(self.data, self.server.payload)
            logging.debug(self.data)
            
            logging.info("Sending data")
            for api in self.server.api:
                response = api(self.data, self.server.reqnum)
                if response: logging.debug(response)
                
        except Exception as e:
            logging.error(e)
        
        self.server.reqnum += 1
        
        logging.info("Done")
