import json
from flaskr.db import get_db
from werkzeug.test import Client
from flask import Flask


def test_register(client: Client, app: Flask):
  response = client.post(
      '/load_script/', json={
          'script': 'print(2)',
          'user_id': 1
      }
  )
  assert response.status_code == 200
  script_id = json.loads(response.get_data(as_text=True))['script_id']
  response = client.post(
      '/create_game/', json={
          'script_id': script_id,
          'user_id': 1
      }
  )
  assert response.status_code == 200
  game_id = json.loads(response.get_data(as_text=True))['game_id']
  assert isinstance(game_id, int)
  with app.app_context():
    assert get_db().execute("SELECT id FROM games WHERE user_id == ?;",
                            [1]).fetchone()['id'] == game_id
