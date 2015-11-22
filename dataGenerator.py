import tornado.web
import tornado.httpserver

import subprocess
import json
import os

import Settings
import fileHandler

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")
    def get_prbfilename(self):
        return self.get_secure_cookie("prbFileName")
    def getLasDatFileName(self):
        try:
            name = self.get_secure_cookie("lastDatFileName")
            return name
        except:
            return

class Downloader(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        fileName = self.get_argument("fileName")
        fileName = fileName.split(".")[0]
        fH = fileHandler.FileHandler(self.current_user)
        path = fH.findDataDownloadLink(fileName = fileName, prbFilename = self.get_prbfilename())
        self.write(json.dumps(path))

class Load(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        fileName = self.get_argument('Data')
        f = open(Settings.UPLOAD_LOCATION + self.current_user + '/' +\
                 Settings.DAT_FILE_LOCATION + self.get_prbfilename() + '/' + fileName, 'r')
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
        f = open(Settings.UPLOAD_LOCATION + self.current_user + '/' +\
                 Settings.DAT_FILE_LOCATION + self.get_prbfilename() + '/' + fileName, 'w')
        f.write(data)
        f.close()
        self.write("File Saved")
        #self.redirect('/upload/?fileName=' + fileName)

class FileExecution(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        fileName = self.get_argument('fileName')
        action = self.get_argument('action')
        #destdir = "." + Settings.DOWNLOAD_LOCATION + self.current_user + '/'
        path = Settings.UPLOAD_LOCATION + self.current_user + '/'
        codePath = os.getcwd() + Settings.DOWNLOAD_LOCATION + self.current_user + '/' + self.get_prbfilename() + Settings.muoPrefix +  "/"
        dataPath = os.getcwd() + "/" + Settings.UPLOAD_LOCATION + self.current_user + '/' + Settings.DAT_FILE_LOCATION +\
                    self.get_prbfilename() + "/" 

        f = open(path + "resultantFile", 'w')
        #msg = subprocess.call(["python", path + "executeForData.py"], stderr=f, stdout=f)
        if action == "executeForData":
            msg = subprocess.call(["python3", "executeForData.py", codePath, dataPath + fileName], stderr=f, stdout=f)
            f.close()
            if msg == 0:
                zipPath = codePath + "data" + "/" #fileName.split(".")[0]
                #zipPath = "." + Settings.DOWNLOAD_LOCATION + self.current_user + "/" #some problem here
                f = open(path + "resultantFile", 'a')
                folderName = fileName.split(".")[0]
                msg = subprocess.call(["zip", '-r', zipPath + folderName + ".zip", zipPath + folderName], stderr=f, stdout=f)
                #if msg == 0:
                #    subprocess.call(["mkdir", "-p", Settings.UPLOAD_LOCATION + self.current_user + "/" + Settings.DAT_FILE_LOCATION + fileName.split(".")[0]])
                f.close()

        elif action == "executeForCode":
            self.write("wrong instruction received, probably a javascript error !")
        
        f.close()
        f = open(path + "resultantFile", 'r')
        data = f.read()
        data = json.dumps(data)
        self.write(data)
   
class codeGen(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        fileName = self.getLasDatFileName()
        self.prbLoc = self.get_prbfilename()
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.dat"], Settings.DAT_FILE_LOCATION + self.prbLoc + "/")
        
#         listOfFiles = []
        filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.current_user + '/'
#         
        if not fileName:
            data = 'No data file selected.'
        else:
            fileReader = open(filePathtoUserDirectory + fileName, "r")
            data = fileReader.read()
                
        var = {"data" : data}
        flist = { "fileNames" : f.listOfFiles, "currentDatFile": "", "currentFile": self.get_prbfilename()}#, "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip"}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("dataGen.html", arg = var, arg2 = flist)

    def post(self):
        fileinfo = self.request.files['file'][0]
        fname = fileinfo['filename']
        cname = str(fname)
        datPath = Settings.UPLOAD_LOCATION + self.current_user + "/" + Settings.DAT_FILE_LOCATION + self.get_prbfilename() + "/"
        fh = open( datPath + cname, 'w')
        fh.write(fileinfo['body'])
        fh.close()
        
        #data = open(datPath + cname, 'r').read()
        #data = json.dumps(data)
        
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.dat"], absolutePath=datPath)
                 
        var = {"data" : ""}
        flist = { "fileNames" : f.listOfFiles, "currentDatFile": fname, "currentFile": self.get_prbfilename()}#, "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip"}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("dataGen.html", arg = var, arg2 = flist)
