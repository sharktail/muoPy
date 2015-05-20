import logging
import Settings
import logging.config

class logger(object):
    def __init__(self, name = Settings.mainLogger):
        logging.basicConfig(filename = Settings.loggerPath + name, level=logging.DEBUG, format='%(asctime)s :: %(message)s')
    
    def writeInfo(self, msg):
        logging.info(msg)
        
    def writeDebug(self, msg):
        logging.debug(msg)
    
    def writeWarning(self, msg):
        logging.warning(msg)

class logConfig(object):
    def __init__(self):
        
        logging.config.fileConfig(Settings.loggerPath + 'logging.conf')

        # create logger
        logger = logging.getLogger('simpleExample')