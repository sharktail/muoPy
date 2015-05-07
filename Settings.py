import os
import uuid
dirname = os.path.dirname(__file__)

STATIC_PATH = os.path.join(dirname, 'static')
TEMPLATE_PATH = os.path.join(dirname, 'templates')
COOKIE_SECRET = str(uuid.uuid4())
UPLOAD_LOCATION = "uploads/"

host = "localhost"
user = "root"
passwd = "narayan"
db = "muoPy"

#Logger info
loggerPath = "loggers/"
mainLogger = "mainLogger.log"