import Settings
import glob
import subprocess
import shutil 
import os

class FileHandler(object):
    def __init__(self, username):
        self.username = username;
        self.listOfFiles = []
        self.pathToDownloadDir = os.path.join(Settings.DOWNLOAD_LOCATION[1:], self.username)
        self.browserPathToDownloadDir = os.path.join(Settings.DOWNLOAD_LOCATION, self.username)
        self.filePathtoUserDirectory = os.path.join(Settings.UPLOAD_LOCATION, self.username)
        
    def createFolder(self):
        path = os.path.join(Settings.UPLOAD_LOCATION, self.username)
        subprocess.call(["mkdir", path])
    
    def fileTree(self, fileTypes, additionalPath="", branchFileTypes=["*"], branchPath = ""):
        self.someFiles(fileTypes, additionalPath)
        datFileLoc = os.path.join(self.filePathtoUserDirectory, branchPath)
        res = {}
        for each in self.listOfFiles:
            if os.path.isdir(os.path.join(datFileLoc, each.split(".")[0])) :
                d = self.someFiles(branchFileTypes, os.path.join(branchPath, each.split(".")[0], ""), \
                                   "", response=True)
                res[each] = d
            else:
                res[each] = []
        return res
    
    def someFiles(self, fileTypes, additionalPath="", absolutePath="", response=False):
        #filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.username + '/'
        if absolutePath != "":
            path = absolutePath
        else:
            path = os.path.join(self.filePathtoUserDirectory, additionalPath)
        
        res = []
        for name in fileTypes:
            #files = glob.glob(path + name)
            files = sorted(glob.glob(os.path.join(path, name)), key=os.path.getmtime, reverse=True)

            for each in files:
                #self.listOfFiles.append(each.split('/')[-1])
                res.append(each.split('/')[-1])
        if response:
            return res
        else:
            self.listOfFiles = res
    
    def allFileFolders(self):
        #filePathtoUserDirectory = Settings.UPLOAD_LOCATION + self.username + '/'
        files = glob.glob(os.path.join(self.filePathtoUserDirectory, "*"))
        
        for each in files:
            self.listOfFiles.append(each.split('/')[-1])
            
    def filterFiles(self):
        newList = []
        
        for l in self.listOfFiles:
            check = os.path.isfile(l)
            if check:
                newList.append(l)
        
        return newList
    
    def findDataFiles(self, prbFileName="", prefix=Settings.muoPrefix):
        if prbFileName=="":
            return 0
        else:
            fName = prbFileName.split(".")[0] + prefix
            directory = os.path.join(self.filePathtoUserDirectory, fName)
        
    def zipFolder(self, sourceList, destination):
        #path = os.path.join(Settings.UPLOAD_LOCATION, self.username) 
        #f = open(path + "resultantFile", 'w')
        try:
            msg = shutil.make_archive(destination, 'zip', root_dir=sourceList, base_dir='.')
        except OSError:
            return -1
        else:
            return destination + ".zip"

    def findDownloadLink(self, filename):
        if os.path.isfile(os.path.join(self.pathToDownloadDir, filename)):
            return os.path.join(self.browserPathToDownloadDir, filename)
        else:
            return None

    def findDataDownloadLink(self, fileName, prbFilename):
        path = os.path.join(self.pathToDownloadDir, prbFilename + Settings.muoPrefix, "data")
        if os.path.isdir(os.path.join(path, fileName)):
            if os.path.isfile(os.path.join(path, fileName) + ".zip"):
                return "/" + os.path.join(path, fileName) + ".zip"
            else:
                result = self.zipFolder(os.path.join(path, fileName), os.path.join(path, fileName))
                if result == -1:
                    return None
                else:
                    return "/" + result
        return None
    
    def deletePrbAndDat(self, prbFileName=None):
        if not prbFileName:
            return
        prbFilePath = prbFileName.split(".")[0]
        path = os.path.join( Settings.UPLOAD_LOCATION, self.username, Settings.DAT_FILE_LOCATION, prbFilePath)
        prbFile = os.path.join(self.filePathtoUserDirectory, Settings.PRB_FILE_LOCATION, prbFileName)
        try:
            subprocess.call(["rm", "-rf", path])
            subprocess.call(["rm",  prbFile])
            return 0
        except:
            return -1
    
    def returnPRBLoc(self, prbFileName):
        path = os.path.join( Settings.UPLOAD_LOCATION, self.username, Settings.DAT_FILE_LOCATION, prbFileName)
        return path  
         
if __name__ == "__main__":
    pass
