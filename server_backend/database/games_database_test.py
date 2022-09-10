from server_backend.database.games_database import *


class TestGamesDatabase:
  def _get_db(self) -> sqlite3.Connection:
    DB_SETUP_SCRIPT_PATH = './flaskr/schema.sql'
    db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    with open(DB_SETUP_SCRIPT_PATH, 'r') as f:
      db.executescript(f.read())
    return db

  def _add_game(
      self, db: sqlite3.Connection, user_id: int, script_id: int
  ) -> int:
    game_id = add_game(db, user_id, script_id)
    assert isinstance(game_id, int)
    assert script_id == get_script_id(db, game_id)
    return game_id

  def _remove_game(self, db: sqlite3.Connection, game_id: int):
    assert remove_game(db, game_id)
    assert not remove_game(db, game_id)
    assert get_script_id(db, game_id) is None

  def test_create_db(self):
    db = self._get_db()
    db.execute('SELECT 1')

  def test_add_game(self):
    db = self._get_db()
    self._add_game(db, 1, 1)
    self._add_game(db, 2, 2)
    self._add_game(db, 1, 2)

  def test_remove_game(self):
    db = self._get_db()
    first_id = self._add_game(db, 1, 1)
    self._remove_game(db, first_id)
    second_id = self._add_game(db, 1, 1)
    third_id = self._add_game(db, 2, 2)
    fourth_id = self._add_game(db, 3, 2)
    self._remove_game(db, third_id)
    self._remove_game(db, second_id)
    self._remove_game(db, fourth_id)
