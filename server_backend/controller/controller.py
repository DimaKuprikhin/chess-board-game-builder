import pathlib
import sqlite3
from server_backend.database import games_database
from server_backend.database import scripts_database
from server_backend.script_checker import script_checker
from server_backend.common import utils
from typing import Any, Tuple


class Controller:
  def __init__(self, base_module_name: str, scripts_dir: pathlib.PosixPath):
    self.base_module_name = base_module_name
    self.scripts_dir = scripts_dir

  def create_game(self, db: sqlite3.Connection, user_id: int,
                  script_id: int) -> Tuple[bool, Any]:
    '''
    Creates a game that uses script with the given script id. Script id must be
    a result of previously called `load_script`. If scripts database doesn't
    contain a script with the given `script_id`, returns False and error
    message. Otherwise, returns True and `game_id` that must be used for futher
    requests.
    '''
    if not scripts_database.contains(db, script_id):
      return False, 'There is no script with this script id: ' + str(script_id)
    link = utils.generate_unique_string(8)
    return True, {
        'game_id': games_database.add_game(db, user_id, script_id, link),
        'link': link
    }

  def load_script(self, db: sqlite3.Connection, user_id: int,
                  script: str) -> Tuple[bool, Any]:
    '''
    Calls by flask frontend to check user script and save it to database, if it
    is valid. On success, returns True status and script id, which should be
    used for futher requests. On failure, returns False status and failure
    message.
    '''
    if not script_checker.check_script(script):
      return False, 'Script didn\'t manage to pass security check'
    return True, scripts_database.add_script(
        db, user_id, script, self.base_module_name, self.scripts_dir
    )
