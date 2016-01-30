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
    
    def fileTree(self, fileTypes, additionalPath="", branchFileTypes=["*"], branchPath = ""):
        self.someFiles(fileTypes, additionalPath)
        datFileLoc = self.filePathtoUserDirectory + branchPath
        res = {}
        for each in self.listOfFiles:
            if os.path.isdir(datFileLoc + each.split(".")[0]) :
                d = self.someFiles(branchFileTypes, branchPath + each.split(".")[0] + "/", "", response=True)
                res[each] = d
            else:
                res[each] = []
        return res
    
    def someFiles(self, fileTypes, additionalPath="", absolutePath="", response=False):
        #filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.username + '/'
        if absolutePath != "":
            path = absolutePath
        else:
            path = self.filePathtoUserDirectory + additionalPath
        
        res = []
        for name in fileTypes:
            files = glob.glob(path + name)
            for each in files:
                #self.listOfFiles.append(each.split('/')[-1])
                res.append(each.split('/')[-1])
        if response:
            return res
        else:
            self.listOfFiles = res
    
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
        path = Settings.UPLOAD_LOCATION + self.username + '/' 
        f = open(path + "resultantFile", 'w')
        msg = subprocess.call(["zip", '-r', destination + ".zip", sourceList], stderr=f, stdout=f)
        if msg == 0:
            return destination + ".zip"
        else:
            return -1

    def findDownloadLink(self, filename):
        if os.path.isfile(self.pathToDownloadDir[1:] + filename):
            return self.pathToDownloadDir + filename
        else:
            return None

    def findDataDownloadLink(self, fileName, prbFilename):
        path = self.pathToDownloadDir[1:] + prbFilename + Settings.muoPrefix + "/" + "data" + "/"
        print path
        if os.path.isdir(path + fileName):
            if os.path.isfile(path + fileName + ".zip"):
                return "/" + path + fileName + ".zip"
            else:
                result = self.zipFolder(path + fileName, path + fileName)
                if result == -1:
                    return None
                else:
                    return "/" + result
        print "path not found"
        return None
        
if __name__ == "__main__":
    pass