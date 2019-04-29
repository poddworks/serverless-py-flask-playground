import os
from environment import *

APP_SECRET = bytes.fromhex(os.environ.get("FLASK_APP_SECRET"))