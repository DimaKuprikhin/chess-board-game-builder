import json
import pathlib
from flask import Blueprint, request, current_app
from flaskr import db, utils
from server_backend.controller.controller import Controller

get_game_state_bp = Blueprint(
    'get_game_state', __name__, url_prefix='/get_game_state'
)


@get_game_state_bp.route('/', methods=['GET'])
def get_game_state():
  if request.content_length >= 1024 * 1024:
    return json.dumps({ 'status': False, 'message': 'Data too large'})
  request_json = json.loads(
      request.get_data(cache=False, as_text=True, parse_form_data=False)
  )

  controller = Controller(
      'scripts', pathlib.PosixPath('.', 'scripts'),
      current_app.config.get('INIT_BY_TEST', False)
  )
  game_id = request_json['game_id']

  status, result = controller.get_game_state(db.get_db(), game_id)

  if status:
    return {
        'status': status,
        'result': {
            'pieces': result['pieces'],
            'possible_moves': result['possible_moves']
        }
    }
  return { 'status': status, 'result': result }
