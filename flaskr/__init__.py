import os

from flask import Flask
from flaskr import create_game
from flaskr import db
from flaskr import join_by_link
from flaskr import load_script
from flaskr import get_game_state
from flaskr import make_move


# application factory
def create_app(test_config=None):
  # create the flask instance
  # __name__: name of the current python module. Used to set up paths.
  # instance_ralative_config: configuration paths are relative to the instance folder.
  app = Flask(__name__, instance_relative_config=True)
  # sets some configurations that the app will use
  # SECRET_KEY: used by Flask to keep data safe. Should be overridden when deploying.
  # DATABASE: path where the database file will be saved.
  app.config.from_mapping(
      SECRET_KEY='dev',
      DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )
  app.config['SCRIPTS_DIR'] = './scripts'
  app.config['BASE_MODULE_NAME'] = 'scripts'

  if test_config is None:
    # load the instance config, if it exists, when not testing
    # for example, it can be used to set the real secret key when deploying.
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  db.init_app(app)

  app.register_blueprint(load_script.load_script_bp)
  app.register_blueprint(create_game.create_game_bp)
  app.register_blueprint(join_by_link.join_by_link_bp)
  app.register_blueprint(make_move.make_move_bp)
  app.register_blueprint(get_game_state.get_game_state_bp)
  return app
