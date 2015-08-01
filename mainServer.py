import tornado.web
import tornado.httpserver
import subprocess
import json
import md5

import Settings
import dbCon
import fileHandler

myDb = dbCon.datacon()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class Test(BaseHandler):
    def get(self):
        arg = self.get_argument("fileOptions")
        self.render("test.html", arg = arg)

class FileExecution(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("You are not supposed to be here")
        
    def post(self):
        fileName = self.get_argument('fileName')
        path = Settings.UPLOAD_LOCATION + self.current_user + '/' 
        #f = open(path, 'w')
        #f.write(data)
        #f.close()
        
        f = open(path + "resultantFile", 'w')
        msg = subprocess.call(["python", path + fileName], stderr=f, stdout=f)
        f.close()
        if msg == 0:
            f = open(path + "resultantFile", 'a')
            subprocess.call(["zip", '-r', Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "cmpc.zip","cmpc"], stderr=f, stdout=f)
            f.close()
        f = open(path + "resultantFile", 'r')
        data = f.read()
        data = json.dumps(data)
        self.write(data)

class Load(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        #Meant for Loading a file
        fileName = self.get_argument('Data')
        f = open(Settings.UPLOAD_LOCATION + self.current_user + '/' + fileName, 'r')
        data = f.read()
        data = json.dumps(data)
        self.write(data)
        
    def get(self):
        self.write("You are not supposed to be here")
        
class Save(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("You are not supposed to be here")
        
    def post(self):
        #Meant for saving a file from the editor
        data = self.get_argument('Data')
        fileName = self.get_argument('fileName')
        f = open(Settings.UPLOAD_LOCATION + self.current_user + '/' + fileName, 'w')
        f.write(data)
        f.close()

class Upload(BaseHandler):
    @tornado.web.authenticated
    def get(self, fileName=None):
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.py","*.txt"])
        
#         listOfFiles = []
        filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.current_user + '/'
#         
        if not fileName:
            data = 'No files selected.'
        else:
            f = open(filePathtoUserDirectory,"r")
            data = f.read()
#         
#         pys = glob.glob(filePathtoUserDirectory + '*.py')
#         for each in pys:
#             listOfFiles.append(each.split('/')[-1])
#         
#         txts =  glob.glob(filePathtoUserDirectory + '*.txt')
#         for each in txts:
#             listOfFiles.append(each.split('/')[-1])  
            
             
        var = {"data" : data}
        flist = { "fileNames" : f.listOfFiles, "currentFile": ""}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("upload.html", arg = var, arg2 = flist)
        
    def post(self):
        #Need to put try except for empty filearg
        fileinfo = self.request.files['filearg'][0]
        fname = fileinfo['filename']
        
        #extn = os.path.splitext(fname)[1]
        #cname = str("lastfile") + extn
        cname = str(fname)
        fh = open(Settings.UPLOAD_LOCATION + self.current_user + "/" + cname, 'w')
        fh.write(fileinfo['body'])
        fh.close()
        
        data= fileinfo['body']
        data = data.replace('\n', '&#13;&#10;')
        data = data.replace('"', '\u0022')
        data = data.replace("'", '\u0027')
        
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.py","*.txt"])  
                 
        var = {"data" : data}
        flist = { "fileNames" : f.listOfFiles, "currentFile": fname, "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "cmpc.zip"}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("upload.html", arg = var, arg2 = flist)

class loginHandler(BaseHandler):
    # Need to define a logout method
    def get(self):
        if not self.current_user:
            self.redirect('/')
        elif self.current_user:
            self.redirect('/upload/')
        
    def post(self):
        username = self.get_argument('username')
        password = md5.md5( self.get_argument('password')).digest()
        #querry = 'Select Password from Users where UserName = %s;'
        querry = 'select u.Password, a.Path from Users as u Join AccountInfo as a on u.id=a.User_Id where u.UserName = %s;'
        resp = myDb.fetchOne(querry, (username))
        if not resp:
            self.write("Username not found. Forgot username? Ask the admin")
        else:
            dBpass = resp[0]
            dBPathToDirectory = resp[1]
            if dBpass == password :
                self.set_secure_cookie("username", username)
                self.redirect('/upload/')
                #self.render("index.html", username = username)
            else:
                self.write("Wrong Password. Forgot password? Ask the admin")

class makeUser(BaseHandler):
    def createUser(self):
        querry = 'Insert into Users(Username, Password, LastName, FirstName, Email, Address, City)\
                     values(%s, %s, %s, %s, %s, %s, %s);'
        resp = myDb.run(querry, (self.username, self.password, self.lastname, self.firstname, self.email, "OVGU", "Magdeburg"))
        if resp:
            try:
                subprocess.call(["mkdir", Settings.UPLOAD_LOCATION + self.username])
                subprocess.call(["mkdir", Settings.DOWNLOAD_LOCATION + self.username])
                querry = 'select Id from Users where UserName = %s;'
                resp = myDb.fetchOne(querry, (self.username) )
                UserId = resp[0]
                querry = 'Insert into AccountInfo(User_Id, Path) Values(%s, %s);'
                resp = myDb.run(querry, (UserId, Settings.UPLOAD_LOCATION + self.username))
                self.set_secure_cookie("username", self.username)
                self.render("index.html", username = self.username)
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
        self.createUser()
        
         
class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            var = {"firstname":"Tony", "lastname":"Stark", "path":"test", "filename":"hello.txt" } # example to be removed
            v = json.dumps(var)
            self.render("hello.html", arg=v)
        else:
            self.redirect('/upload/')
            

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler),
            (r"/login/?", MainHandler),
            (r"/signin/?", loginHandler),
            (r"/signup/?", makeUser),
            (r"/upload/?", Upload),
            (r"/upload/save?", Save),
            (r"/upload/load?", Load),
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
