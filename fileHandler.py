import Settings
import glob
import subprocess
import os

class FileHandler(object):
    def __init__(self, username):
        self.username = username;
        self.listOfFiles = []
    
    def createFolder(self):
        path = Settings.UPLOAD_LOCATION + "/" + self.username
        subprocess.call(["mkdir", path])
    
    def someFiles(self, userName, fileTypes):
        filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.userName + '/'
        
        for name in fileTypes:
            files = glob.glob(filePathtoUserDirectory + name)
        
        for each in files:
            self.listOfFiles.append(each.split('/')[-1])
    
    def allFileFolders(self):
        
        filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.userName + '/'
        
        files = glob.glob(filePathtoUserDirectory + "*")
        
        for each in files:
            self.listOfFiles.append(each.split('/')[-1])
            
    def filterFiles(self):
        newList = []
        
        for l in self.listOfFiles:
            check = os.path.isfile(l)
            if check:
                newList.append(l)
        
        return newList