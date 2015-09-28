import tornado.web
import tornado.httpserver

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class codeGen(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("codeGen.html")
        
class dataGen(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("Hello")