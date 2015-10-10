import tornado.web
import tornado.httpserver

import subprocess
import json

import Settings
import fileHandler

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class codeGen(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        
        fileName = self.get_argument("fileName", default=None)
        f = fileHandler.FileHandler(self.current_user)
        f.findDataFiles(fileName)
        self.write(json.dumps(fileName))