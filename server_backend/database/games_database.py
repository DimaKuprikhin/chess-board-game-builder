import sqlite3


def add_game(db: sqlite3.Connection, user_id: int, script_id: int) -> int:
  '''
  Adds a new entry in the database. Returns game id.
  '''
  db.execute(
      'INSERT INTO games (user_id, script_id) VALUES (?, ?);',
      [user_id, script_id]
  )
  db.commit()
  # TODO: is there some better way to do it?
  return db.execute('SELECT id FROM games ORDER BY id DESC LIMIT 1;'
                    ).fetchone()['id']


def get_script_id(db: sqlite3.Connection, game_id: int) -> int:
  '''
  Returns script id of the entry with the giver game id. If the database
  doesn't contain an entry with this game id, returns None.
  '''
  result = db.execute('SELECT script_id FROM games WHERE id == ?;',
                      [game_id]).fetchone()
  return None if result is None else result['script_id']


def remove_game(db: sqlite3.Connection, game_id: int) -> bool:
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
