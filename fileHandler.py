import Settings
import glob
import subprocess
import os

class FileHandler(object):
    def __init__(self, username):
        self.username = username;
        self.listOfFiles = []
        self.filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.username + '/'
        
    def createFolder(self):
        path = Settings.UPLOAD_LOCATION + "/" + self.username
        subprocess.call(["mkdir", path])
    
    def someFiles(self, fileTypes, additionalPath=""):
        #filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.username + '/'
        self.filePathtoUserDirectory = self.filePathtoUserDirectory + additionalPath
        
        for name in fileTypes:
            files = glob.glob(self.filePathtoUserDirectory + name)
            for each in files:
                self.listOfFiles.append(each.split('/')[-1])
    
    def allFileFolders(self):
        #filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.username + '/'
        files = glob.glob(self.filePathtoUserDirectory + "*")
        
        for each in files:
            self.listOfFiles.append(each.split('/')[-1])
            
    def filterFiles(self):
        newList = []
        
        for l in self.listOfFiles:
            check = os.path.isfile(l)
            if check:
                newList.append(l)
        
        return newList
    
    def zipFolder(self, sourceList, destination):
        print "Here the folders will be zipped"

if __name__ == "__main__":
    pass