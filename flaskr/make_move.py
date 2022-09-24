import json
import pathlib
from flask import Blueprint, request, current_app
from flaskr import db
from server_backend.controller.controller import Controller

make_move_bp = Blueprint('make_move', __name__, url_prefix='/make_move')


@make_move_bp.route('/', methods=['POST'])
def make_move():
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
  user_id = request_json['user_id']
  move = request_json['move']

  status, result = controller.make_move(db.get_db(), game_id, user_id, move)
  return { 'status': status, 'result': result }
