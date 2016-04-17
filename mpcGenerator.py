import tornado.web
import tornado.httpserver

import subprocess
import shutil
import json
import os

from muaompc._ldt.parse import prbdsl
import Settings
import fileHandler
import loggerHandler

log = loggerHandler.logger()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        #return self.get_secure_cookie("username").decode()
        username = self.get_secure_cookie("username")
        if username:
            username = username.decode()
        return username

class Downloader(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        fileName = self.get_argument("fileName")
        fileName = fileName.split(".")[0] + Settings.muoPrefix + ".zip"
        fH = fileHandler.FileHandler(self.current_user)
        path = fH.findDownloadLink(fileName)
        self.write(json.dumps(path))

class createOrDeleteFile(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #deletes prb file from disc and corresponding directory for dat files
        fileName = self.get_argument("fileName")
        if fileName.split(".").__len__()==1:
            fileName = fileName + ".prb"
        fH = fileHandler.FileHandler(self.current_user)
        msg = fH.deletePrbAndDat(fileName)
            
        if msg==0:
            self.write("success")
        else:
            self.write("failed")
    
    @tornado.web.authenticated
    def post(self):
        #creates new prb file
        fileName = self.get_argument("fileName")
        fileName = fileName + '.prb'
        filePath = os.path.join(Settings.UPLOAD_LOCATION, self.current_user, \
                                Settings.PRB_FILE_LOCATION, fileName)
        f = open(filePath, "w")
        f.close()
        self.redirect('/codegen/?currentFile=' + fileName)

class Load(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        #reads the content of a prb file and sends the syntax of it
        fileName = self.get_argument('Data')
        filePath = os.path.join(Settings.UPLOAD_LOCATION, self.current_user,\
                 Settings.PRB_FILE_LOCATION, fileName)
        f = open(filePath, 'r')
        data = f.read()
        data = prbdsl.get_syntax_highlight(data)
        data = json.dumps(data)
        self.write(data)
    
    @tornado.web.authenticated    
    def get(self):
        #reads the data and provides the syntax information
        code = self.get_argument('Code')
        data = prbdsl.get_syntax_highlight(code)
        data = json.dumps(data)
        self.write(data)

class Save(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect("/codegen/")
        
    def post(self):
        #Meant for saving a file from the editor
        data = self.get_argument('Data')
        fileName = self.get_argument('fileName')
        filePath = os.path.join(Settings.UPLOAD_LOCATION, self.current_user,\
                 Settings.PRB_FILE_LOCATION, fileName)
        f = open(filePath, 'w')
        f.write(data)
        f.close()
        self.write(json.dumps("File Saved"))

class FileExecution(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #executes a orb code and generates a zip file from the result
        #sends the msg of code generation
        fileName = self.get_argument('fileName')
        action = self.get_argument('action')
        destdir = os.path.join(Settings.DOWNLOAD_LOCATION[1:], self.current_user)
        path = os.path.join(Settings.UPLOAD_LOCATION, self.current_user) 
        if action == "executeForCode":
            f = open(os.path.join(path, "resultantFile"), 'w')
            msg = subprocess.call(["python3", "executeForCode.py", os.path.join(path, Settings.PRB_FILE_LOCATION, fileName) , destdir], stderr=f, stdout=f)
            f.close()
            if msg == 0:
                zipPath = os.path.join(Settings.DOWNLOAD_LOCATION[1:], self.current_user)
                folderName = fileName.split(".")[0] + Settings.muoPrefix
                try:
                    zipfile = shutil.make_archive(os.path.join(zipPath, folderName), 'zip', root_dir=zipPath, base_dir=folderName)
                except OSError:
                    log.writeDebug("Error in zipping file")
            else:
                log.writeDebug("Prb File exucation caused error in shell")
                subprocess.call(["mkdir", "-p", os.path.join(Settings.UPLOAD_LOCATION, self.current_user, Settings.DAT_FILE_LOCATION, fileName.split(".")[0])])

        elif action == "executeForData":
            self.write("wrong instruction received, probably a javascript error !")
        
        f = open(os.path.join(path, "resultantFile"), 'a')
        f.write("End of Prb File " + fileName + " Execution")
        f.close()
        f = open(os.path.join(path, "resultantFile"), 'r')
        data = f.read()
        data = json.dumps(data)
        self.write(data)
        
    def post(self):
        self.redirect("/codegen/")


class codeGen(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #Upon redirected codegen page it sends the codegen html along 
        #with the file tree structure for the user
        fileName = self.get_argument("fileName", default=None)
            
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.prb"], Settings.PRB_FILE_LOCATION)
        
#         listOfFiles = []
        filePathtoUserDirectory = os.path.join(Settings.UPLOAD_LOCATION, self.current_user)
     
        if not fileName:
            data = 'No file selected.'
        else:
            fileReader = open(os.path.join(filePathtoUserDirectory, fileName),"r")
            data = fileReader.read()
            
        fileTree = f.fileTree(["*.prb"], Settings.PRB_FILE_LOCATION, ["*.dat"], Settings.DAT_FILE_LOCATION)
        
        var = {"data" : data}
        currentFile = ""
        currentDatFile = ""
        try:
            currentFile = self.get_argument("currentFile")
            try:
                currentDatFile = self.get_argument("currentDatFile")
            except:
                pass
        except:
            pass
        flist = { "fileTree": fileTree, "fileNames" : f.listOfFiles, "currentFile": currentFile, "currentDatFile": currentDatFile}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("codeGen.html", arg = var, arg2 = flist)

    def post(self):
        #Method to handle the request when a file is uploaded
        #Should be deprecated if not required afterwards
        fileinfo = self.request.files['filearg'][0]
        fname = fileinfo['filename']
        
        cname = str(fname)
        filePath = os.path.join(Settings.UPLOAD_LOCATION, self.current_user, Settings.PRB_FILE_LOCATION)
        fh = open(os.path.join(filePath, cname), 'w')
        fh.write(fileinfo['body'])
        fh.close()
        
        #data = open(Settings.UPLOAD_LOCATION + self.current_user + "/" + Settings.PRB_FILE_LOCATION + cname, 'r').read()
        #data = json.dumps(data)
        
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.prb"], Settings.PRB_FILE_LOCATION)
        fileTree = f.fileTree(["*.prb"], Settings.PRB_FILE_LOCATION, ["*.dat"], Settings.DAT_FILE_LOCATION)
        
        var = {"data" : ""}
        flist = {"fileTree": fileTree, "fileNames" : f.listOfFiles, "currentFile": fname}#, "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip"}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("codeGen.html", arg = var, arg2 = flist)
