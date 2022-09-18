import json
from flaskr.db import get_db
from werkzeug.test import Client
from flask import Flask


def test_register(client: Client, app: Flask):
  script = open('./server_backend/test_data/chess_rules.py').read()
  response = client.post(
      '/load_script/', json={
          'script': script,
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
  response = json.loads(response.get_data(as_text=True))
  assert response['status']
  response = response['result']
  link = response['link']
  game_id = response['id']

  response = client.post('/join_by_link/', json={ 'link': link, 'user_id': 2 })
  assert response.status_code == 200
  response = json.loads(response.get_data(as_text=True))
  assert response['status']
  with app.app_context():
    query_result = get_db().execute(
        'SELECT first_player_id, second_player_id FROM games WHERE id == ?;',
        [game_id]
    ).fetchone()
    assert query_result['first_player_id'] == 1
    assert query_result['second_player_id'] == 2
