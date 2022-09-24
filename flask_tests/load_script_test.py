import json
from flaskr.db import get_db
from werkzeug.test import Client
from flask import Flask


def test_load_script(client: Client, app: Flask):
  response = client.post(
      '/load_script/', json={
          'script': 'print(2)',
          'user_id': 1
      }
  )
  assert response.status_code == 200
  script_id = json.loads(response.get_data(as_text=True)
                         )['result']['script_id']
  assert isinstance(script_id, int)
  with app.app_context():
    assert get_db().execute(
        "SELECT id FROM scripts WHERE id == ?;", [script_id]
    ).fetchone() is not None
