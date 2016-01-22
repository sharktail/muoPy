import MySQLdb as sql
import Settings
from loggerHandler import logger
log = logger()
class datacon(object):
    def __init__(self):
        self.db = sql.connect(host = Settings.host, user = Settings.user, passwd = Settings.passwd, db = Settings.db)
        #self.cur = self.db.cursor()
        
    def run(self, querry, tup):
        try:
            cur = self.db.cursor()
            cur.execute(querry, tup)
            self.save()
        except Exception as e:
            log.writeDebug("Error at dbCon run: " + e.__str__()) 
            self.db.rollback()
            return False
        return True
    
    def fetchAll(self, querry, tup):
        try:
            cur = self.db.cursor()
            cur.execute(querry, tup)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            log.writeDebug("Error at dbCon fetchAll: " + e.__str__()) 
            return False
    
    def fetchOne(self, querry, tup):
        try:
            cur = self.db.cursor()
            cur.execute(querry, tup)
            return cur.fetchone()
        except Exception as e:
            log.writeDebug("Error at dbCon fetchOne: " + e.__str__()) 
            return False
        
    def save(self):
        try:
            self.db.commit()
            return True
        except:
            print "Fatal Error in Commiting"
            return False