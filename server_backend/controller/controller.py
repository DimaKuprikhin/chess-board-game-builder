import json
import pathlib
import sqlite3
from server_backend.database import game_dto
from server_backend.database import games_database
from server_backend.database import scripts_database
from server_backend.executer import executer_host
from server_backend.script_checker import script_checker
from server_backend.common import utils
from typing import Any, Tuple


class Controller:
  def __init__(
      self,
      base_module_name: str,
      scripts_dir: pathlib.PosixPath,
      init_by_test=False
  ):
    self.base_module_name = base_module_name
    self.scripts_dir = scripts_dir
    self.init_by_test = init_by_test

  def create_game(self, db: sqlite3.Connection,
                  game: game_dto.GameDTO) -> Tuple[bool, Any]:
    '''
    Creates a game that uses script with the given script id. Script id must be
    a result of previously called `load_script`. If scripts database doesn't
    contain a script with the given `script_id`, returns False and error
    message. Otherwise, returns True and `game_id` that must be used for futher
    requests.
    '''
    if not scripts_database.contains(db, game.get_script_id()):
      return False, 'There is no script with this script id: ' + str(
          game.get_script_id()
      )
    game_id = games_database.add_entry(
        db, game.set_link(utils.generate_unique_string(8))
    )
    return True, games_database.get_entry(db, game_id)

  def join_by_link(
      self, db: sqlite3.Connection, link: str, second_player_id: int
  ) -> Tuple[bool, Any]:
    game = games_database.get_entries_by_predicate(
        db, 'link == ? AND second_player_id IS NULL', [link]
    )
    if len(game) == 0:
      return False, 'There is no game to which you can join by link ' + link
    game = game[0]

    games_database.update_entry(
        db, game.set_second_player_id(second_player_id)
    )
    script_id = game.get_script_id()
    module_name = scripts_database.get_module_name(db, script_id)
    host = executer_host.ExecuterHost(self.init_by_test)
    host.create_executer()
    status, result = host.call_script_function(
        module_name, 'get_starting_state', [], 0.1
    )
    host.finish()
    if status:
      games_database.update_entry(db, game.set_game_state(json.dumps(result)))
      color = 'white' if game.get_first_player_plays_as(
      ) == 'black' else 'black'
      return status, {
          'game_state': result,
          'game_id': game.get_id(),
          'color': color,
          'turn': 'white'
      }
    return False, result

  def load_script(self, db: sqlite3.Connection,
                  script: str) -> Tuple[bool, Any]:
    '''
    Calls by flask frontend to check user script and save it to database, if it
    is valid. On success, returns True status and script id, which should be
    used for futher requests. On failure, returns False status and failure
    message.
    '''
    if not script_checker.check_script(script):
      return False, 'Script didn\'t manage to pass validation check'
    return True, scripts_database.add_script(
        db, script, self.base_module_name, self.scripts_dir
    )

  def make_move(
      self, db: sqlite3.Connection, game_id: int, user_id: int, move: map
  ) -> Tuple[bool, Any]:
    game = games_database.get_entry(db, game_id)
    if game is None:
      return False, 'There is no game with this id'

    if move == 'resign':
      winning_user_color = game.get_first_player_plays_as()
      if game.get_first_player_id() == user_id:
        winning_user_color = 'white' if winning_user_color == 'black' else 'black'
      resigned_user_color = 'white' if winning_user_color == 'black' else 'black'
      game_state = json.loads(game.get_game_state())
      game_state['possible_moves'] = []
      game_state['status'] = winning_user_color + ' won'
      games_database.update_entry(
          db, game.set_game_state(json.dumps(game_state))
      )
      return True, {
          'game_state': game_state,
          'color': resigned_user_color,
          'turn': 'white'
      }

    # TODO: needs testing.
    if self._check_for_draw(game):
      game_state = json.loads(game.get_game_state())
      game_state['possible_moves'] = []
      game_state['status'] = 'draw'
      games_database.update_entry(
          db, game.set_game_state(json.dumps(game_state))
      )
      color = game.get_first_player_plays_as()
      if user_id != game.get_first_player_id():
        color = 'white' if color == 'black' else 'black'
      return True, { 'game_state': game_state, 'color': color, 'turn': 'white'}

    script_id = game.get_script_id()
    module_name = scripts_database.get_module_name(db, script_id)
    if module_name is None:
      return False, 'There is no module with this id'

    # Call make_move in script.
    host = executer_host.ExecuterHost(self.init_by_test)
    if not host.create_executer():
      return False, 'Couldn\t create executer'
    game_state = json.loads(game.get_game_state())
    pieces = game_state['pieces']
    additional_data = game_state['additional_data']
    next_turn = 'white' if game.get_move_number() % 2 == 1 else 'black'
    status, result = host.call_script_function(
        module_name, 'make_move', [pieces, move, next_turn, additional_data],
        0.1
    )
    host.finish()

    if status:
      # Update game state in database.
      game.set_move_number(game.get_move_number() + 1)
      games_database.update_entry(db, game.set_game_state(json.dumps(result)))
    color = game.get_first_player_plays_as()
    if user_id != game.get_first_player_id():
      color = 'white' if color == 'black' else 'black'
    return status, { 'game_state': result, 'color': color, 'turn': next_turn }

  def get_game_state(self, db: sqlite3.Connection, game_id: int,
                     user_id: int) -> Tuple[bool, Any]:
    game = games_database.get_entry(db, game_id)
    if game is None:
      return False, 'There is no game with this id'
    color = game.get_first_player_plays_as()
    if user_id != game.get_first_player_id():
      color = 'white' if color == 'black' else 'black'
    turn = 'white' if game.get_move_number() % 2 == 0 else 'black'
    game_state = game.get_game_state()
    if game_state is None:
      game_state = '{"pieces": [], "possible_moves": [], "additional_data": {}, "status": "not started"}'
    return True, {
        'game_state': json.loads(game_state),
        'color': color,
        'turn': turn
    }

  def _check_for_draw(self, game: game_dto.GameDTO) -> bool:
    return game.get_move_number() >= 200
