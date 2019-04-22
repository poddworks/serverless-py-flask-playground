import os

# the values of those depend on your setup
POSTGRES_URL = os.environ.get("DATABASE_URI")
POSTGRES_USER = os.environ.get("DATABASE_USER")
POSTGRES_PW = os.environ.get("DATABASE_PASSWD")
POSTGRES_DB = os.environ.get("DATABASE_DB_NAME")

# simple app secret for encrypt and decrypt
APP_SECRET = bytes.fromhex(os.environ.get("FLASK_APP_SECRET"))
BLOCK_SIZE = 16 # this is the encryption block size for AES