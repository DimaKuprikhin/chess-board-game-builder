import flask
import os
import pytest
import tempfile
from flaskr.db import init_db
import flaskr


@pytest.fixture
def app():
  db_fd, db_path = tempfile.mkstemp()
  scripts_dir = './server_backend/test_data/scripts_dir'
  base_module_name = 'server_backend.test_data.scripts_dir'
  app = flaskr.create_app({
      'TESTING': True,
      'DATABASE': db_path,
      'SCRIPTS_DIR': scripts_dir,
      'BASE_MODULE_NAME': base_module_name,
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
