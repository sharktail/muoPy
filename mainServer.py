import tornado.web
import tornado.httpserver
import Settings

class loginHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        print username, password
        self.render("index.html")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("hello.html")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/login/?", MainHandler),
            (r"/signin/?", loginHandler)
        ]
        settings = {
            "template_path": Settings.TEMPLATE_PATH,
            "static_path": Settings.STATIC_PATH,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(8888)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
