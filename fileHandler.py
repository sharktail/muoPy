import Settings
import glob
import subprocess
import os

class FileHandler(object):
    def __init__(self, username):
        self.username = username;
        self.listOfFiles = []
        self.pathToDownloadDir = Settings.DOWNLOAD_LOCATION + self.username + "/"
        self.filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.username + '/'
        
    def createFolder(self):
        path = Settings.UPLOAD_LOCATION + "/" + self.username
        subprocess.call(["mkdir", path])
    
    def someFiles(self, fileTypes, additionalPath="", absolutePath=""):
        #filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.username + '/'
        if absolutePath != "":
            path = absolutePath
        else:
            path = self.filePathtoUserDirectory + additionalPath
        
        for name in fileTypes:
            files = glob.glob(path + name)
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
    
    def findDataFiles(self, prbFileName="", prefix="_bcg"):
        if prbFileName=="":
            return 0
        else:
            fName = prbFileName.split(".")[0] + prefix
            directory = self.filePathtoUserDirectory + fName + '/'
        
    def zipFolder(self, sourceList, destination):
        print "Here the folders will be zipped"

    def findDownloadLink(self, filename):
        if os.path.isfile(self.pathToDownloadDir[1:] + filename):
            return self.pathToDownloadDir + filename
        else:
            return None
        
if __name__ == "__main__":
    pass