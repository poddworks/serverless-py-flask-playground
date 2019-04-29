import os

# database connection settings
POSTGRES_URL = os.environ.get("DATABASE_URI", 'localhost')
POSTGRES_USER = os.environ.get("DATABASE_USER", 'postgres')
POSTGRES_PW = os.environ.get("DATABASE_PASSWD", None)
POSTGRES_DB = os.environ.get("DATABASE_DB_NAME", 'postgres')

# cache connection settings
REDIS_URI = os.environ.get("CACHE_URI", 'localhost')
REDIS_PORT = int(os.environ.get("CACHE_PORT", 6379))
RESIS_DB_NAME = int(os.environ.get("CACHE_DB_NAME", 0))

# AWS Simple Queue Service settings
AWS_SQS_URI = os.environ.get('AWS_SQS_QUEUE_URI')

# simple app secret for encrypt and decrypt
APP_SECRET = bytes.fromhex(os.environ.get("FLASK_APP_SECRET"))
BLOCK_SIZE = 16 # this is the encryption block size for AES
