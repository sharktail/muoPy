import os
import uuid
dirname = os.path.dirname(__file__)

STATIC_PATH = os.path.join(dirname, 'static')
TEMPLATE_PATH = os.path.join(dirname, 'templates')
COOKIE_SECRET = str(uuid.uuid4())