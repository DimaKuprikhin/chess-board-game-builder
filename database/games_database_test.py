from database.games_database import *


class TestGamesDatabase:
  def _create_db(self) -> GamesDatabase:
    db = GamesDatabase()
    assert db.get_game_state(1) is None
    assert db.get_script_id(1) is None
    assert not db.update_game_state(1, None)
    assert not db.remove_game(1)
    return db

  def _add_game(
      self, db: GamesDatabase, user_id: int, script_id: int, game_state
  ):
    assert db.add_game(user_id, script_id, game_state)
    assert script_id == db.get_script_id(user_id)
    assert game_state == db.get_game_state(user_id)
    assert not db.add_game(user_id, 0, None)
    assert script_id == db.get_script_id(user_id)
    assert game_state == db.get_game_state(user_id)

  def _remove_game(self, db: GamesDatabase, user_id: int):
    assert db.remove_game(user_id)
    assert not db.remove_game(user_id)
    assert not db.get_game_state(user_id)
    assert not db.get_script_id(user_id)

  def test_create_db(self):
    self._create_db()

  def test_add_game(self):
    db = self._create_db()
    self._add_game(db, 1, 1, '')
    self._add_game(db, 2, 2, '')
    # Add game with the existing script id.
    self._add_game(db, 3, 2, '')

  def test_remove_game(self):
    db = self._create_db()
    self._add_game(db, 1, 1, '')
    self._remove_game(db, 1)
    self._add_game(db, 1, 1, '')
    self._add_game(db, 2, 2, '')
    self._add_game(db, 3, 2, '')
    self._remove_game(db, 2)
    self._remove_game(db, 3)
    self._remove_game(db, 1)
