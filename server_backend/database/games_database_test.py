from copy import deepcopy
import json
from server_backend.database.games_database import add_entry, get_entry, remove_entry, update_entry
from server_backend.database.game_dto import GameDTO
import sqlite3


class TestGamesDatabase:
  def _get_db(self) -> sqlite3.Connection:
    DB_SETUP_SCRIPT_PATH = './flaskr/schema.sql'
    db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    with open(DB_SETUP_SCRIPT_PATH, 'r') as f:
      db.executescript(f.read())
    return db

  def _add_entry(self, db: sqlite3.Connection, entry: GameDTO) -> int:
    game_id = add_entry(db, entry)
    entry_ = deepcopy(entry)
    entry_.set_id(game_id)
    assert isinstance(game_id, int)
    assert entry_ == get_entry(db, game_id)
    return game_id

  def _remove_entry(self, db: sqlite3.Connection, game_id: int):
    assert remove_entry(db, game_id)
    assert not remove_entry(db, game_id)
    assert get_entry(db, game_id) is None

  def test_create_db(self):
    db = self._get_db()
    db.execute('SELECT 1')

  def test_add_entry(self):
    db = self._get_db()
    self._add_entry(
        db,
        GameDTO(
            first_player_ip='1',
            first_player_plays_as='white',
            move_number=0,
            turn='white',
            script_id=1,
            link='link'
        )
    )
    self._add_entry(
        db,
        GameDTO(
            first_player_ip='2',
            first_player_plays_as='black',
            move_number=1,
            turn='black',
            script_id=2,
            link='link2'
        )
    )
    self._add_entry(
        db,
        GameDTO(
            first_player_ip='1',
            first_player_plays_as='white',
            move_number=2,
            turn='white',
            script_id=2,
            link='link3'
        )
    )

  def test_remove_entry(self):
    db = self._get_db()
    first_id = self._add_entry(
        db,
        GameDTO(
            first_player_ip='1',
            first_player_plays_as='black',
            move_number=3,
            turn='black',
            script_id=1,
            link='link'
        )
    )
    self._remove_entry(db, first_id)
    second_id = self._add_entry(
        db,
        GameDTO(
            first_player_ip='1',
            first_player_plays_as='white',
            move_number=4,
            turn='white',
            script_id=1,
            link='link2'
        )
    )
    third_id = self._add_entry(
        db,
        GameDTO(
            first_player_ip='2',
            first_player_plays_as='white',
            move_number=5,
            turn='black',
            script_id=2,
            link='link3'
        )
    )
    fourth_id = self._add_entry(
        db,
        GameDTO(
            first_player_ip='2',
            first_player_plays_as='black',
            move_number=5,
            turn='white',
            script_id=2,
            link='link4'
        )
    )
    self._remove_entry(db, third_id)
    self._remove_entry(db, second_id)
    self._remove_entry(db, fourth_id)

  def test_update_entry(self):
    db = self._get_db()
    entry = GameDTO(
        first_player_ip='1',
        first_player_plays_as='white',
        move_number=6,
        turn='black',
        script_id=100,
        link='unique_link'
    )
    game_id = self._add_entry(db, entry)
    entry = get_entry(db, game_id)
    entry.set_additional_data(json.dumps({ 'key': 'value'}))
    update_entry(db, entry)
    assert entry == get_entry(db, game_id)
