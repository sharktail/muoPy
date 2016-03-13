import tornado.web
import tornado.httpserver
import subprocess
import json
import md5

import Settings
import dbCon
import fileHandler
import mpcGenerator
import dataGenerator
import loggerHandler


log = loggerHandler.logger()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        #this reads the secured cookie and if username is found
        # current_user is set which accounts for logged in users
        return self.get_secure_cookie("username")

class logoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #it clears the cookie to log the user out
        self.clear_cookie("username")
        self.render("home.html", arg=None)

class loginHandler(BaseHandler):
    def get(self):
        #if the user cookie is found then user
        #is redirected to the codegen page
        if not self.current_user:
            self.redirect('/')
        elif self.current_user:
            self.redirect('/codegen/')
        
    def post(self):
        #reads username and checks password for authentication
        myDb = dbCon.datacon()
        username = self.get_argument('username')
        password = md5.md5( self.get_argument('password')).digest()
        querry = 'select u.Password, a.Path from Users as u Join AccountInfo as a on u.id=a.User_Id where u.UserName = %s;'
        resp = myDb.fetchOne(querry, (username,))
        if not resp:
            self.render("home.html", arg = {"msg":"Username not found. Forgot username? Ask the admin"})
        else:
            dBpass = resp[0]
            if dBpass == password :
                self.set_secure_cookie("username", username)
                self.redirect('/codegen/')
            else:
                self.render("home.html", arg = {"msg":"Wrong Password"})

class makeUser(BaseHandler):
    def createUser(self):
        #this method handles user sign ups
        #it creates a user login for the new users
        myDb = dbCon.datacon()
        querry = 'select Password from Users where UserName = %s;'
        resp = myDb.fetchOne(querry, (self.username,))
        
        if resp != None:
            self.render("home.html", arg = {"msg":"Username already exists."})
            self.finish()
        
        querry = 'Insert into Users(Username, Password, LastName, FirstName, Email, Address, City)\
                     values(%s, %s, %s, %s, %s, %s, %s);'
        resp = myDb.run(querry, (self.username, self.password, self.lastname, self.firstname, self.email, "OVGU", "Magdeburg"))
        if resp:
            try:
                subprocess.call(["mkdir", "-p", Settings.UPLOAD_LOCATION + self.username])
                subprocess.call(["mkdir", "-p", Settings.UPLOAD_LOCATION + self.username + "/datFiles"])
                subprocess.call(["mkdir", "-p",Settings.UPLOAD_LOCATION + self.username + "/prbFiles"])
                subprocess.call(["mkdir", "-p", "."+Settings.DOWNLOAD_LOCATION + self.username])
                querry = 'select Id from Users where UserName = %s;'
                resp = myDb.fetchOne(querry, (self.username,) )
                UserId = resp[0]
                querry = 'Insert into AccountInfo(User_Id, Path) Values(%s, %s);'
                resp = myDb.run(querry, (UserId, Settings.UPLOAD_LOCATION + self.username))
                self.set_secure_cookie("username", self.username)
                #self.render("index.html", username = self.username)
                self.redirect("/codegen/")
            except:
                self.write("Error in creating Directory !!! \nNo worries, contact the admin.")
        else:
            self.write("Fatal Error in Creating user in Database !!! \nNo worries, contact the admin.")
    def get(self):
        self.write("Invalid link: Only Post requests.")
    
    def post(self):
        self.email = self.get_argument('email')
        self.username = self.get_argument('username')
        self.password = md5.md5(self.get_argument('password')).digest()
        self.lastname = self.get_argument('lastname')
        self.firstname = self.get_argument('firstname')
        
        if self.username in [None, ""] or self.get_argument('password') in [None, ""]:
            self.render("home.html", arg = {"msg":"Username/Password field empty."})
            self.finish()
        
        self.createUser()
        
         
class MainHandler(BaseHandler):
    def get(self):
        #if previously logged in it directly directs to codegen
        #or redirects to login page
        if not self.current_user:
            self.render("home.html", arg=None)
        else:
            self.redirect('/codegen/')
            

class Application(tornado.web.Application):
    # Creating the URLs for the server
    def __init__(self):
        handlers = [
            (r"/?", MainHandler),
            (r"/login/?", MainHandler),
            (r"/logout/?", logoutHandler),
            (r"/signin/?", loginHandler),
            (r"/signup/?", makeUser),
            (r"/createNewPRB/?", mpcGenerator.createOrDeleteFile),
            (r"/codegen/?", mpcGenerator.codeGen),
            (r"/codegen/save/?", mpcGenerator.Save),
            (r"/codegen/load/?", mpcGenerator.Load),
            (r"/codegen/datagen/?", mpcGenerator.Redirect),
            (r"/codegen/execute/?", mpcGenerator.FileExecution),
            (r"/codegen/delete/?", mpcGenerator.createOrDeleteFile),
            (r"/codegen/downloadlink/?", mpcGenerator.Downloader),
            (r"/datagen/createNewFile/?", dataGenerator.createOrDeleteFile),
            (r"/datagen/?", dataGenerator.codeGen),
            (r"/datagen/save/?", dataGenerator.Save),
            (r"/datagen/load/?", dataGenerator.Load),
            (r"/datagen/execute/?", dataGenerator.FileExecution),
            (r"/datagen/delete/?", dataGenerator.createOrDeleteFile),
            (r"/datagen/downloadlink/?", dataGenerator.Downloader),
            (r"/test?", mpcGenerator.codeGen)
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
    http_server.listen(Settings.portNumber)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
