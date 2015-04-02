import tornado.web
import tornado.httpserver
import Settings
import json
from tornado.escape import xhtml_escape

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class loginHandler(BaseHandler):
    # Need to define a logout method
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        print username, password, Settings.COOKIE_SECRET
        self.set_secure_cookie("username", username)
        self.render("index.html", username = username)


class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            var = {"firstname":"Sankar", "lastname":"Datta"}
            v = json.dumps(var)
            #v = xhtml_escape(v)
            sh = "hellooo"
            sh = xhtml_escape(sh)
            self.render("hello.html", arg=v)
        else:
            #kwargs = {'name' : self.current_user}
            #self.render("index.html", **kwargs)
            self.render("index.html", username = self.current_user)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/login/?", MainHandler),
            (r"/signin/?", loginHandler)
        ]
        settings = {
            "template_path": Settings.TEMPLATE_PATH,
            "static_path": Settings.STATIC_PATH,
            "cookie_secret": Settings.COOKIE_SECRET,
            "login_url": "/login"
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(8888)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
