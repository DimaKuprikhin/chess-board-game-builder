import json
import pathlib
from flask import Blueprint, request
from flaskr import db
from server_backend.controller.controller import Controller

load_script_bp = Blueprint('load_script', __name__, url_prefix='/load_script')


@load_script_bp.route('/', methods=['POST'])
def load_script():
  if request.content_length >= 1024 * 1024:
    return (400, 'Data is too big')
  user_id, script = deserialize_load_script_request(
      request.get_data(cache=False, as_text=True, parse_form_data=False)
  )
  controller = Controller('scripts', pathlib.PosixPath('.', 'scripts'))
  status, result = controller.load_script(db.get_db(), user_id, script)
  if status:
    return serialize_load_script_response(result)
  return (400, result)


def deserialize_load_script_request(request):
  print(request)
  request = json.loads(request)
  return request['user_id'], request['script']


def serialize_load_script_response(script_id):
  return json.dumps({ 'script_id': script_id })
