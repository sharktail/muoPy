import tornado.web
import tornado.httpserver

import subprocess
import json

import Settings
import fileHandler

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class Redirect(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        fileName = self.get_argument("fileName")
        self.set_secure_cookie("prbFileName", fileName)
        self.redirect("/datagen")
        #self.write("success")

class Load(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        fileName = self.get_argument('Data')
        f = open(Settings.UPLOAD_LOCATION + self.current_user + '/' +\
                 Settings.PRB_FILE_LOCATION + fileName, 'r')
        data = f.read()
        data = json.dumps(data)
        self.write(data)
        
    def get(self):
        self.write("You are not supposed to be here")

class Save(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("Get Request received instead of Post")
        
    def post(self):
        #Meant for saving a file from the editor
        data = self.get_argument('Data')
        fileName = self.get_argument('fileName')
        f = open(Settings.UPLOAD_LOCATION + self.current_user + '/' +\
                 Settings.PRB_FILE_LOCATION + fileName, 'w')
        f.write(data)
        f.close()
        self.write("File Saved")
        #self.redirect('/upload/?fileName=' + fileName)

class FileExecution(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        fileName = self.get_argument('fileName')
        action = self.get_argument('action')
        destdir = "." + Settings.DOWNLOAD_LOCATION + self.current_user + '/'
        path = Settings.UPLOAD_LOCATION + self.current_user + '/' 
        f = open(path + "resultantFile", 'w')
        #msg = subprocess.call(["python", path + "executeForData.py"], stderr=f, stdout=f)
        if action == "executeForCode":
            msg = subprocess.call(["python3", "executeForCode.py", path + Settings.PRB_FILE_LOCATION + fileName , destdir], stderr=f, stdout=f)
            f.close()
            if msg == 0:
                zipPath = "." + Settings.DOWNLOAD_LOCATION + self.current_user + "/"
                f = open(path + "resultantFile", 'a')
                folderName = fileName.split(".")[0] + "_bcg"
                msg = subprocess.call(["zip", '-r', zipPath + folderName + ".zip", zipPath + folderName], stderr=f, stdout=f)
                if msg == 0:
                    subprocess.call(["mkdir", "-p", Settings.UPLOAD_LOCATION + self.current_user + "/" + Settings.DAT_FILE_LOCATION + fileName.split(".")[0]])
                f.close()

        elif action == "executeForData":
            self.write("wrong instruction received, probably a javascript error !")
        
        f.close()
        f = open(path + "resultantFile", 'r')
        data = f.read()
        data = json.dumps(data)
        self.write(data)
        
    def post(self):
#         fileName = self.get_argument('fileName')
#         path = Settings.UPLOAD_LOCATION + self.current_user + '/' 
#         #f = open(path, 'w')
#         #f.write(data)
#         #f.close()
#         
#         f = open(path + "resultantFile", 'w')
#         msg = subprocess.call(["python", path + fileName], stderr=f, stdout=f)
#         f.close()
#         if msg == 0:
#             f = open(path + "resultantFile", 'a')
#             subprocess.call(["zip", '-r', Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip","install_bcg"], stderr=f, stdout=f)
#             f.close()
#         f = open(path + "resultantFile", 'r')
#         data = f.read()
#         data = json.dumps(data)
#        self.write(data)
        self.write("Expecting a get request") 


class codeGen(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        
        fileName = self.get_argument("fileName", default=None)
            
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.prb"], Settings.PRB_FILE_LOCATION)
        
#         listOfFiles = []
        filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.current_user + '/'
#         
        if not fileName:
            data = 'No files selected.'
        else:
            fileReader = open(filePathtoUserDirectory + fileName,"r")
            data = fileReader.read()
            
             
        var = {"data" : data}
        flist = { "fileNames" : f.listOfFiles, "currentFile": "", "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip"}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("codeGen.html", arg = var, arg2 = flist)

    def post(self):
        fileinfo = self.request.files['filearg'][0]
        fname = fileinfo['filename']
        
        cname = str(fname)
        fh = open(Settings.UPLOAD_LOCATION + self.current_user + "/" + Settings.PRB_FILE_LOCATION + cname, 'w')
        fh.write(fileinfo['body'])
        fh.close()
        
        data = open(Settings.UPLOAD_LOCATION + self.current_user + "/" + Settings.PRB_FILE_LOCATION + cname, 'r').read()
        data = json.dumps(data)
        
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.prb"], Settings.PRB_FILE_LOCATION)
                 
        var = {"data" : data}
        flist = { "fileNames" : f.listOfFiles, "currentFile": fname, "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip"}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("codeGen.html", arg = var, arg2 = flist)