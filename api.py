from application import app
from cache import rcli as cache


from flask import Response
from flask import request
from flask import jsonify


import secrets
import json
import datetime
import dateutil.parser
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES


import environment_app as environment

@app.route("/hello", methods=['GET'])
def hello():
  now = datetime.datetime.utcnow()
  lastAccessAt, _ = cache.pipeline().get('lastAccessAt').set('lastAccessAt', str(now)).execute()
  if lastAccessAt is not None:
    lastAccessAt = dateutil.parser.parse(lastAccessAt)
  else:
    lastAccessAt = now
  return Response(response=f'Hello World, Last Seen: {lastAccessAt}, Now: {now}!', status=200, mimetype='text/plain')

@app.route("/timestamp", methods=['GET'])
def timestamp():
  now = datetime.datetime.utcnow()
  return jsonify({'timestamp': now})

@app.route("/me", methods=['GET'])
def me():
  from model import User
  result = None
  try:
    username = request.args.get('username')
    if username is not None:
      result = User.query.filter_by(username=username).first()
    else:
      result = User.query.all()
  except Exception as err:
    return Response(response=str(err), status=500, mimetype='text/plain')
  else:
    if result is None:
      return Response(response='Not-Found', status=404, mimetype='text/plain')
  if type(result) is list:
    return jsonify([r.as_dict() for r in result])
  else:
    return jsonify(result.as_dict())

@app.route("/encrypt", methods=['POST'])
def encrypt():
  result = {'custome_data': None}
  try:
    custom_data = pad(bytes(json.dumps(request.args), 'utf-8'), environment.BLOCK_SIZE)
    iv = secrets.token_bytes(environment.BLOCK_SIZE)
    cipher = AES.new(environment.APP_SECRET, AES.MODE_CBC, iv)
    result['custome_data'] = f'{iv.hex()}.{cipher.encrypt(custom_data).hex()}'
  except Exception as err:
    return Response(response=str(err), status=500, mimetype='text/plain')
  else:
    return jsonify(result)

@app.route("/decrypt", methods=['GET'])
def decrypt():
  content = request.args.get('content')
  result = None
  try:
    if content is None:
      raise Exception(f'Argument "content" is missing')
    iv_hex, encrypted_data_hex = content.split('.')
    cipher = AES.new(environment.APP_SECRET, AES.MODE_CBC, bytes.fromhex(iv_hex))
    data = cipher.decrypt(bytes.fromhex(encrypted_data_hex))
    result = json.loads(unpad(data, environment.BLOCK_SIZE))
  except Exception as err:
    return Response(response=str(err), status=500, mimetype='text/plain')
  else:
    return jsonify(result)

@app.route("/entry", methods=['GET', 'POST'])
def get_entry():
  from model import Entry
  if request.method == 'POST':
    import boto3
    sqs = boto3.client('sqs', region_name=environment.AWS_SQS_REGION)
    try:
      content = request.data[:Entry.content.property.columns[0].type.length].decode('utf-8')
      sqs.send_message(QueueUrl=environment.AWS_SQS_QUEUE_URI, MessageBody=content)
    except Exception as err:
      return Response(response=str(err), status=500, mimetype='text/plain')
    return jsonify({'received_at': datetime.datetime.utcnow()})

  from sqlalchemy import desc
  result = None
  try:
    result = Entry.query.order_by(desc(Entry.created_at)).limit(100).all()
  except Exception as err:
    return Response(response=str(err), status=500, mimetype='text/plain')
  else:
    if result is None:
      return Response(response='Not-Found', status=404, mimetype='text/plain')
  if type(result) is list:
    return jsonify([r.as_dict() for r in result])
  else:
    return jsonify(result.as_dict())
