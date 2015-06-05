import Settings
import subprocess

class FileHandler(object):
    def __init__(self, username):
        self.username = username;
    
    def createFolder(self):
        path = Settings.UPLOAD_LOCATION + "/" + self.username
        subprocess.call(["mkdir", path])