import logging
import Settings

class logger(object):
    def __init__(self, name = Settings.mainLogger):
        logging.basicConfig(filename = Settings.loggerPath + name, level=logging.DEBUG)
    
    def info(self):
        
        