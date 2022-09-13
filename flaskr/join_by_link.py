import json
import pathlib
from flask import Blueprint, request
from flaskr import db, utils
from server_backend.controller.controller import Controller

join_by_link_bp = Blueprint(
    'join_by_link', __name__, url_prefix='/join_by_link'
)


@join_by_link_bp.route('/', methods=['POST'])
def join_by_link():
  if request.content_length >= 1024 * 1024:
    return json.dumps({ 'status': False, 'message': 'Data too large'})
  request_json = json.loads(
      request.get_data(cache=False, as_text=True, parse_form_data=False)
  )

  controller = Controller('scripts', pathlib.PosixPath('.', 'scripts'))
  second_player_ip = utils.get_user_ip(request)
  link = request_json['link']
  result = controller.join_by_link(db.get_db(), link, second_player_ip)
  return { 'status': result }
