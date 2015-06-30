import Settings
import glob
import subprocess

class FileHandler(object):
    def __init__(self, username):
        self.username = username;
    
    def createFolder(self):
        path = Settings.UPLOAD_LOCATION + "/" + self.username
        subprocess.call(["mkdir", path])
    
    def allFiles(self, userName):
        listOfFiles = []
        filePathtoUserDirectory = Settings.UPLOAD_LOCATION + userName + '/'
        pys = glob.glob(filePathtoUserDirectory + '*.py')
        for each in pys:
            listOfFiles.append(each.split('/')[-1])
        
        txts =  glob.glob(filePathtoUserDirectory + '*.txt')
        for each in txts:
            listOfFiles.append(each.split('/')[-1])