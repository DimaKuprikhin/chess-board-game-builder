import sqlite3
from server_backend.database.game_dto import GameDTO


def add_entry(db: sqlite3.Connection, entry: GameDTO) -> int:
  '''
  Adds a new entry in the database. Returns inserted game id. Game id is
  autoincremented, so `entry.id` of this entry is ignored in this method.
  '''
  db.execute(
      'INSERT INTO games (\
        first_player_id, \
        second_player_id, \
        first_player_plays_as, \
        move_number, \
        turn, \
        script_id, \
        link, \
        game_state, \
        additional_data\
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);', [
          entry.get_first_player_id(),
          entry.get_second_player_id(),
          entry.get_first_player_plays_as(),
          entry.get_move_number(),
          entry.get_turn(),
          entry.get_script_id(),
          entry.get_link(),
          entry.get_game_state(),
          entry.get_additional_data()
      ]
  )
  db.commit()
  # TODO: is there some better way to do it?
  return db.execute('SELECT id FROM games ORDER BY id DESC LIMIT 1;'
                    ).fetchone()['id']


def get_entries_by_predicate(
    db: sqlite3.Connection, predicate: str, params: list
) -> list:
  '''
  Returns list of the database entries that satisfied given `predicate`.
  '''
  db_entries = db.execute(
      'SELECT \
        id, \
        first_player_id, \
        second_player_id, \
        first_player_plays_as, \
        move_number, \
        turn, \
        script_id, \
        link, \
        game_state, \
        additional_data \
      FROM games WHERE ' + predicate + ';', params
  ).fetchall()
  entries = []
  for db_entry in db_entries:
    entries.append(
        GameDTO(
            db_entry['id'], db_entry['first_player_id'],
            db_entry['second_player_id'], db_entry['first_player_plays_as'],
            db_entry['move_number'], db_entry['turn'], db_entry['script_id'],
            db_entry['link'], db_entry['game_state'],
            db_entry['additional_data']
        )
    )
  return entries


def get_entry(db: sqlite3.Connection, id: int) -> GameDTO:
  '''
  Returns database entry with id equal to the given `id`. If the database
  doesn't have an entry with this id, returns None.
  '''
  db_entry = db.execute(
      'SELECT \
        id, \
        first_player_id, \
        second_player_id, \
        first_player_plays_as, \
        move_number, \
        turn, \
        script_id, \
        link, \
        game_state, \
        additional_data \
      FROM games WHERE id == ?;', [id]
  ).fetchone()
  if db_entry is None:
    return None
  return GameDTO(
      db_entry['id'], db_entry['first_player_id'],
      db_entry['second_player_id'], db_entry['first_player_plays_as'],
      db_entry['move_number'], db_entry['turn'], db_entry['script_id'],
      db_entry['link'], db_entry['game_state'], db_entry['additional_data']
  )


def remove_entry(db: sqlite3.Connection, game_id: int) -> bool:
  '''
  Removes an entry with the given game id from the database. If the database
  doesn't contain an entry with this game id, returns False and doesn't
  change its state.
  '''
  result = db.execute('SELECT id FROM games WHERE id == ?;',
                      [game_id]).fetchone()
  if result is None:
    return False
  db.execute('DELETE FROM games WHERE id == ?;', [game_id])
  db.commit()
  return True


def update_entry(db: sqlite3.Connection, entry: GameDTO):
  '''
  Updates field of the database row with id equal to `entry.get_id()`.
  Field values of the row will be set to corresponding values from `entry`.
  If the database doesn't contain an entry with this id, nothing is changed.
  '''
  db.execute(
      'UPDATE games SET (\
        first_player_id, \
        second_player_id, \
        first_player_plays_as, \
        move_number, \
        turn, \
        script_id, \
        link, \
        game_state, \
        additional_data\
      ) = (?, ?, ?, ?, ?, ?, ?, ?, ?) WHERE id == ?;', [
          entry.get_first_player_id(),
          entry.get_second_player_id(),
          entry.get_first_player_plays_as(),
          entry.get_move_number(),
          entry.get_turn(),
          entry.get_script_id(),
          entry.get_link(),
          entry.get_game_state(),
          entry.get_additional_data(),
          entry.get_id()
      ]
  )
  db.commit()
