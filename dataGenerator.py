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
        username = self.get_secure_cookie("username")
        if username:
            username = username.decode()
        return username
    
    def get_prbfilename(self):
        prbfileName = self.get_secure_cookie("prbFileName")
        if prbfileName:
            prbfileName = prbfileName.decode()
        return prbfileName
    
    def getLasDatFileName(self):
        try:
            name = self.get_secure_cookie("lastDatFileName")
            if name:
                name = name.decode()
            return name
        except:
            return

class Downloader(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #Sends the download location of data
        fileName = self.get_argument("fileName")
        prbfileName = self.get_argument("PRB")
        fileName = fileName.split(".")[0]
        fH = fileHandler.FileHandler(self.current_user)
        path = fH.findDataDownloadLink(fileName = fileName, prbFilename = prbfileName)
        self.write(json.dumps(path))

class createOrDeleteFile(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        #Creates new dat file
        fileName = self.get_argument("fileName") + ".dat"
        currentFileName = self.get_argument("prbFileName")
        prbFileName = currentFileName.split(".")[0]
        prbDatLocation = os.path.join(Settings.UPLOAD_LOCATION, self.current_user, Settings.DAT_FILE_LOCATION, prbFileName)
        subprocess.call(["mkdir", "-p", prbDatLocation])
        f = open(os.path.join(prbDatLocation, fileName), "w")
        f.close()
        self.redirect("/codegen/?currentFile=" + currentFileName \
                      + "&currentDatFile=" + fileName)
    
    @tornado.web.authenticated
    def get(self):
        # Removes a dat file
        fileName = self.get_argument("fileName")
        prbFileName = self.get_argument("prbFileName")
        fH = fileHandler.FileHandler(self.current_user)
        path = fH.returnPRBLoc(prbFileName)
        datPath = os.path.join(path, fileName)
        msg = subprocess.call(["rm", datPath])
        if msg==0:
            self.write("success")
        else:
            self.write("failed")
    
class Load(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        #Reads a dat file and send the content
        prbfileName = self.get_argument("PRB")
        self.set_secure_cookie("prbFileName", prbfileName)
        fileName = self.get_argument('Data')
        datFilePath = os.path.join(Settings.UPLOAD_LOCATION, self.current_user, Settings.DAT_FILE_LOCATION, prbfileName)
        f = open( os.path.join(datFilePath, fileName), 'r')
        data = f.read()
        data = prbdsl.get_syntax_highlight(data)
        data = json.dumps(data)
        self.write(data)
        
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
        datFilePath = os.path.join(Settings.UPLOAD_LOCATION, self.current_user,\
                                   Settings.DAT_FILE_LOCATION, self.get_prbfilename())
        f = open(os.path.join(datFilePath, fileName), 'w')
        f.write(data)
        f.close()
        self.write(json.dumps("File Saved"))

class FileExecution(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #Executes the data and generates the zip file
        fileName = self.get_argument('fileName')
        
        path = os.path.join(Settings.UPLOAD_LOCATION, self.current_user)
        codePath = os.path.join(Settings.DOWNLOAD_LOCATION[1:], self.current_user, self.get_prbfilename()+Settings.muoPrefix)
        dataPath = os.path.join(os.getcwd(), Settings.UPLOAD_LOCATION, self.current_user,\
                                 Settings.DAT_FILE_LOCATION, self.get_prbfilename())

        f = open(os.path.join(path, "resultantFile"), 'w')
        msg = subprocess.call(["python3", "executeForData.py", codePath, os.path.join(dataPath, fileName)], stderr=f, stdout=f)
        if msg == 0:
            zipPath = os.path.join(codePath, "data")
            folderName = fileName.split(".")[0]
            try:
                shutil.make_archive(os.path.join(zipPath, folderName), 'zip', root_dir=zipPath, base_dir=folderName)
            except OSError:
                log.writeDebug("Error in zipping file")
        
        f.write("End of dat File " + fileName + " Execution")
        f.close()
        f = open(os.path.join(path, "resultantFile"), 'r')
        data = f.read()
        data = json.dumps(data)
        self.write(data)
   
class codeGen(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #Upon redirection sends the datagen html
        fileName = self.getLasDatFileName()
        self.prbLoc = self.get_prbfilename()
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.dat"], Settings.DAT_FILE_LOCATION + self.prbLoc + "/")
        
#         listOfFiles = []
        filePathtoUserDirectory = os.path.join(Settings.UPLOAD_LOCATION, self.current_user)
#         
        if not fileName:
            data = 'No data file selected.'
        else:
            fileReader = open(os.path.join(filePathtoUserDirectory, fileName), "r")
            data = fileReader.read()
                
        var = {"data" : data}
        flist = { "fileNames" : f.listOfFiles, "currentDatFile": "", "currentFile": self.get_prbfilename()}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("dataGen.html", arg = var, arg2 = flist)

    def post(self):
        fileinfo = self.request.files['file'][0]
        fname = fileinfo['filename']
        cname = str(fname)
        datPath = os.path.join(Settings.UPLOAD_LOCATION, self.current_user,\
                               Settings.DAT_FILE_LOCATION, self.get_prbfilename())
        fh = open( datPath + cname, 'w')
        fh.write(fileinfo['body'])
        fh.close()
        
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.dat"], absolutePath=datPath)
                 
        var = {"data" : ""}
        flist = { "fileNames" : f.listOfFiles, "currentDatFile": fname, "currentFile": self.get_prbfilename()}#, "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip"}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("dataGen.html", arg = var, arg2 = flist)
