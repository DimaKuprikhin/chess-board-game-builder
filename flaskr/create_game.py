import json
import pathlib
from flask import Blueprint, request
from flaskr import db
from server_backend.controller.controller import Controller

create_game_bp = Blueprint('create_game', __name__, url_prefix='/create_game')


@create_game_bp.route('/', methods=['POST'])
def create_game():
  if request.content_length >= 1024 * 1024:
    return (400, 'Data is too big')
  request_json = json.loads(
      request.get_data(cache=False, as_text=True, parse_form_data=False)
  )
  controller = Controller('scripts', pathlib.PosixPath('.', 'scripts'))
  status, result = controller.create_game(
      db.get_db(), request_json['user_id'], request_json['script_id']
  )
  if status:
    return json.dumps({ 'game_id': result })
  return (400, result)
