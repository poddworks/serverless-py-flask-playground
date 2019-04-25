import os
import redis
import environment

rcli = None
if os.environ.get('DEPLOY_STATUS', 'development') == 'development':
  rcli = redis.Redis(host=environment.REDIS_URI, port=environment.REDIS_PORT, db=0)
else:
  rcli = redis.Redis(host=environment.REDIS_URI, port=environment.REDIS_PORT, db=environment.RESIS_DB_NAME)