import json
from flaskr.db import get_db
from werkzeug.test import Client
from flask import Flask


def test_make_move(client: Client, app: Flask):
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

  response = client.post(
      '/make_move/',
      json={
          'game_id': game_id,
          'user_id': 1,
          'move': {
              'from_x': 0,
              'from_y': 1,
              'to_x': 0,
              'to_y': 3
          }
      }
  )
  assert response.status_code == 200
  response = json.loads(response.get_data(as_text=True))
  assert response['status']
  result = response['result']
  assert result['color'] == 'white'
  assert result['turn'] == 'black'
