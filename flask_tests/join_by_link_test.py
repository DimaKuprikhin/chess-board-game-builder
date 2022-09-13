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
          'play_as': 'white'
      }
  )
  assert response.status_code == 200
  response = json.loads(response.get_data(as_text=True))
  link = response['link']
  game_id = response['game_id']

  response = client.post('/join_by_link/', json={ 'link': link })
  assert response.status_code == 200
  response = json.loads(response.get_data(as_text=True))
  assert response['status']
  with app.app_context():
    query_result = get_db().execute(
        'SELECT first_player_ip, second_player_ip FROM games WHERE id == ?;',
        [game_id]
    ).fetchone()
    assert query_result['first_player_ip'] == '127.0.0.1'
    assert query_result['second_player_ip'] == '127.0.0.1'
