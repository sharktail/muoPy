import tornado.web
import tornado.httpserver

import subprocess
import json

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
        flist = { "fileNames" : f.listOfFiles, "currentFile": "", "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip"}
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
        
        data = open(datPath + cname, 'r').read()
        data = json.dumps(data)
        
        f = fileHandler.FileHandler(self.current_user)
        f.someFiles(["*.dat"], absolutePath=datPath)
                 
        var = {"data" : data}
        flist = { "fileNames" : f.listOfFiles, "currentFile": fname, "downloadLink": Settings.DOWNLOAD_LOCATION + self.current_user + "/" + "install_bcg.zip"}
        var = json.dumps(var)
        flist = json.dumps(flist)
        self.render("dataGen.html", arg = var, arg2 = flist)