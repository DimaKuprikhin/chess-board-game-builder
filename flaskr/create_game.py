import json
import pathlib
from flask import Blueprint, request
from flaskr import db, utils
from server_backend.controller.controller import Controller
from server_backend.database.game_dto import GameDTO

create_game_bp = Blueprint('create_game', __name__, url_prefix='/create_game')


@create_game_bp.route('/', methods=['POST'])
def create_game():
  if request.content_length >= 1024 * 1024:
    return json.dumps({ 'status': False, 'message': 'Data too large'})
  request_json = json.loads(
      request.get_data(cache=False, as_text=True, parse_form_data=False)
  )

  controller = Controller('scripts', pathlib.PosixPath('.', 'scripts'))
  game = GameDTO(
      first_player_ip=utils.get_user_ip(request),
      first_player_plays_as=request_json['play_as'],
      move_number=0,
      turn='white',
      script_id=request_json['script_id']
  )
  status, result = controller.create_game(db.get_db(), game)

  if status:
    return json.dumps({ 'status': True, 'result': result.to_map() })
  return json.dumps({ 'status': False, 'message': result })
