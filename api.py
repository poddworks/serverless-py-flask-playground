from application import app
from model import User
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


import environment

@app.route("/hello", methods=['GET'])
def hello():
  dt = datetime.datetime
  now = dt.utcnow()
  lastAccessAt, _ = cache.pipeline().get('lastAccessAt').set('lastAccessAt', str(now)).execute()
  if lastAccessAt is not None:
    lastAccessAt = dateutil.parser.parse(lastAccessAt)
  else:
    lastAccessAt = now
  return Response(response=f'Hello World, Last Seen: {lastAccessAt}, Now: {now}!', status=200, mimetype='text/plain')

@app.route("/timestamp", methods=['GET'])
def timestamp():
  dt = datetime.datetime
  return jsonify({'timestamp': dt.utcnow()})

@app.route("/me", methods=['GET'])
def me():
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