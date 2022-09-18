import json
import pathlib
from flask import Blueprint, request, current_app
from flaskr import db, utils
from server_backend.controller.controller import Controller

get_game_state_bp = Blueprint(
    'get_game_state', __name__, url_prefix='/get_game_state'
)


@get_game_state_bp.route('/<int:game_id>/<int:user_id>', methods=['GET'])
def get_game_state(game_id: int, user_id: int):
  controller = Controller(
      'scripts', pathlib.PosixPath('.', 'scripts'),
      current_app.config.get('INIT_BY_TEST', False)
  )

  status, result = controller.get_game_state(db.get_db(), game_id, user_id)
  return { 'status': status, 'result': result }
