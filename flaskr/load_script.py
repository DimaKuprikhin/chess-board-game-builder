import json
import pathlib
from flask import Blueprint, current_app, request
from flaskr import db
from server_backend.controller.controller import Controller

load_script_bp = Blueprint('load_script', __name__, url_prefix='/load_script')


@load_script_bp.route('/', methods=['POST'])
def load_script():
  if request.content_length >= 1024 * 1024:
    return json.dumps({ 'status': False, 'message': 'Data too large'})
  request_json = json.loads(
      request.get_data(cache=False, as_text=True, parse_form_data=False)
  )
  controller = Controller(
      current_app.config['BASE_MODULE_NAME'],
      pathlib.PosixPath(current_app.config['SCRIPTS_DIR'])
  )

  status, result = controller.load_script(db.get_db(), request_json['script'])

  if status:
    return json.dumps({ 'status': True, 'result': { 'script_id': result } })
  return json.dumps({ 'status': False, 'result': result })
