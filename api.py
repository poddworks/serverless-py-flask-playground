from application import app
from model import User


from flask import Response
from flask import request
from flask import jsonify


@app.route("/hello", methods=['GET'])
def hello():
  return Response(response='Hello World!', status=200, mimetype='text/plain')

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
