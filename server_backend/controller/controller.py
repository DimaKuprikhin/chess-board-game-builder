import pathlib
from typing import Any, Tuple
from server_backend.database import games_database
from server_backend.database import scripts_database
from server_backend.script_checker import script_checker


class Controller:
  def __init__(self):
    self.games_db = None
    self.script_checker = script_checker.ScriptChecker()
    self.scripts_db = None

  def create_game(self, user_id: int, script_id: int,
                  game_state) -> Tuple[bool, str]:
    '''
    Creates a game that uses script with the given script id. User id is used
    as a primary key for games and it means that one user can't create more
    than one game at the same time. Script id must be a result of previously
    called `load_script`. On success returns True, otherwise False and failure
    message.
    '''
    assert self.games_db
    assert self.scripts_db
    if not self.scripts_db.contains(script_id):
      return False, 'Can\'t create a game with incorrect script id'
    if not self.games_db.add_game(user_id, script_id, game_state):
      return False, 'The same user can\'t create multiple games at the same time'
    return True, 'OK'

  def init_games_database(self):
    '''
    Initializes games database. Must be called only once for each Controller.
    '''
    assert not self.games_db
    self.games_db = games_database.GamesDatabase()

  def init_scripts_database(self, data_dir: pathlib.PosixPath):
    '''
    Initializes scripts database in the given directory path. Must be called
    only once for each Controller.
    '''
    assert not self.scripts_db
    self.scripts_db = scripts_database.ScriptsDatabase(
        data_dir, 'user_scripts'
    )

  def load_script(self, script: str) -> Tuple[bool, Any]:
    '''
    Calls by flask frontend to check user script and save it to database, if it
    is valid. On success, returns true status and script id, which should be
    used for futher requests. On failure, returns false status and failure
    message. `init_scripts_database` must be called before this method.
    '''
    assert self.scripts_db
    if not self.script_checker.check_script(script):
      return False, 'Script hasn\'t managed to pass validation check'
    script_id = self.scripts_db.add_script(script)
    return True, script_id
