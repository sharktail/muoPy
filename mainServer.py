import tornado.web
import tornado.httpserver

import os, uuid
__UPLOADS__ = "uploads/"
import Settings
import json
import md5
import dbCon

myDb = dbCon.datacon()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'w')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)

class loginHandler(BaseHandler):
    # Need to define a logout method
    def get(self):
        if not self.current_user:
            var = {"firstname":"Sankar", "lastname":"Datta"} # example to be removed
            v = json.dumps(var)
            self.render("hello.html", arg = v)
        elif self.current_user:
            self.render("index.html", username = self.current_user)
        
    def post(self):
        username = self.get_argument('username')
        password = md5.md5( self.get_argument('password')).digest()
        querry = 'Select Password from Users where UserName = %s;'
        resp = myDb.fetchone(querry, (username))
        if not resp:
            self.write("Username not found. Forgot username? Ask the admin")
        else:
            dBpass = resp[0]
            if dBpass == password :
                self.set_secure_cookie("username", username)
                self.render("index.html", username = username)
            else:
                self.write("Wrong Password. Forgot password? Ask the admin")

class makeUser(BaseHandler):
    def get(self):
        self.write("Invalid link: Only Post requests.")
    
    def post(self):
        email = self.get_argument('email')
        username = self.get_argument('username')
        password = md5.md5(self.get_argument('password')).digest()
        lastname = self.get_argument('lastname')
        firstname = self.get_argument('firstname')
        querry = 'Insert into Users(Username, Password, LastName, FirstName, Email, Address, City)\
                     values(%s, %s, %s, %s, %s, %s, %s);'
        resp = myDb.run(querry, (username, password, lastname, firstname, email, "OVGU", "Magdeburg"))
        if resp:
            self.set_secure_cookie("username", username)
            self.render("index.html", username = username)
        else:
            self.write("Fatal Error in Creating user in Database !!! \nNo worries, contact the admin.")
         
class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            var = {"firstname":"Sankar", "lastname":"Datta"} # example to be removed
            v = json.dumps(var)
            self.render("hello.html", arg=v)
        else:
            #kwargs = {'name' : self.current_user}
            #self.render("index.html", **kwargs)
            self.render("index.html", username = self.current_user)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/login/?", MainHandler),
            (r"/signin/?", loginHandler),
            (r"/signup/?", makeUser),
            (r"/upload/?", Upload)
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
