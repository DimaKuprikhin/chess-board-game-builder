import flask
import os
import pytest
import tempfile
from flaskr.db import init_db
import flaskr


@pytest.fixture
def app():
  db_fd, db_path = tempfile.mkstemp()
  app = flaskr.create_app({
      'TESTING': True,
      'DATABASE': db_path,
  })
  with app.app_context():
    init_db()
  yield app
  os.close(db_fd)
  os.unlink(db_path)


@pytest.fixture
def client(app: flask.Flask):
  return app.test_client()


@pytest.fixture
def runner(app: flask.Flask):
  return app.test_cli_runner()
