import tornado.web
import tornado.httpserver
import os
import subprocess
import json
import md5

import Settings
import dbCon
#import fileHandler

myDb = dbCon.datacon()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class Test(BaseHandler):
    def get(self):
        self.render("test.html")

class FileExecution(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("You are not supposed to be here")
        
    def post(self):
        data = self.get_argument('Data')
        f = open(Settings.UPLOAD_LOCATION + "executefile.py", 'w')
        f.write(data)
        f.close()
        
        f = open(Settings.UPLOAD_LOCATION + "resultantFile", 'w')
        subprocess.call(["python3", Settings.UPLOAD_LOCATION + "executefile.py"], stderr=f, stdout=f)
        f.close()
        f = open(Settings.UPLOAD_LOCATION + "resultantFile", 'r')
        data = f.read()
        data = json.dumps(data)
        self.write(data)
        
class SaveAndLoad(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("You are not supposed to be here.")
    def post(self):
        data = self.get_argument('Data')
        f = open(Settings.UPLOAD_LOCATION + "lastfile.txt", 'w')
        f.write(data)
        f.close()

class Upload(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        f = open(Settings.UPLOAD_LOCATION + "lastfile.txt", 'r')
        data= f.read()
        data = data.replace('\n', '&#13;&#10;')
        f.close()
        var = {"data" : data}
        var = json.dumps(var)
        self.render("upload.html", arg = var)
        
    def post(self):
        #Need to put try except for empty filearg
        fileinfo = self.request.files['filearg'][0]
        fname = fileinfo['filename']
        
        extn = os.path.splitext(fname)[1]
        cname = str("lastfile") + extn
        fh = open(Settings.UPLOAD_LOCATION + cname, 'w')
        fh.write(fileinfo['body'])
        fh.close()
        
        data= fileinfo['body']
        data = data.replace('\n', '&#13;&#10;')
        var = {"data" : data}
        var = json.dumps(var)
        self.render("upload.html", arg = var)

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
            var = {"firstname":"Sankar", "lastname":"Datta", "path":"test", "filename":"hello.txt" } # example to be removed
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
            (r"/upload/?", Upload),
            (r"/upload/save?", SaveAndLoad),
            (r"/upload/execute?", FileExecution),
            (r"/test?", Test)
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
