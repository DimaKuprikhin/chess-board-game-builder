import json
from flaskr.db import get_db
from werkzeug.test import Client
from flask import Flask


def test_create_game(client: Client, app: Flask):
  response = client.post(
      '/load_script/', json={
          'script': 'return 2',
          'user_id': 1
      }
  )
  assert response.status_code == 200
  script_id = json.loads(response.get_data(as_text=True)
                         )['result']['script_id']
  response = client.post(
      '/create_game/',
      json={
          'script_id': script_id,
          'play_as': 'white',
          'user_id': 1
      }
  )
  assert response.status_code == 200
  result = json.loads(response.get_data(as_text=True))
  assert result['status']
  result = result['result']
  assert isinstance(result['id'], int)
  assert isinstance(result['link'], str)
  with app.app_context():
    assert get_db().execute(
        'SELECT id FROM games WHERE first_player_id == 1;'
    ).fetchone()['id'] == result['id']
