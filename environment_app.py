import os
import json
from environment import *

APP_SECRET = bytes.fromhex(os.environ.get("FLASK_APP_SECRET"))

AUTHORIZER_DEBUG = {}
if os.environ.get('DEPLOY_STATUS', 'development') == 'development':
  with open('./dist/identity.json', 'r') as fp:
    AUTHORIZER_DEBUG = json.load(fp)
