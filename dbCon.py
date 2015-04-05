import MySQLdb as sql
import Settings

class datacon(object):
    def __init__(self):
        self.db = sql.connect(host = Settings.host, user = Settings.user, passwd = Settings.passwd, db = Settings.db)
        self.cur = self.db.cursor()
        
    def run(self, querry, tup):
        try:
            self.cur.execute(querry, tup)
            self.save()
        except:
            self.db.rollback()
            return False
        return True
    
    def fetchone(self, querry, tup):
        try:
            self.cur.execute(querry, tup)
            return self.cur.fetchone()
        except:
            return False
        
    def save(self):
        try:
            self.db.commit()
            return True
        except:
            print "Fatal Error in Commiting"
            return False