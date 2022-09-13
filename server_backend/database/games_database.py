import sqlite3


def add_game(
    db: sqlite3.Connection, first_player_ip: str, first_player_play_as: str,
    script_id: int, link: str
) -> int:
  '''
  Adds a new entry in the database. Returns game id.
  '''
  db.execute(
      'INSERT INTO games (first_player_ip, first_player_play_as, script_id, link) VALUES (?, ?, ?, ?);',
      [first_player_ip, first_player_play_as, script_id, link]
  )
  db.commit()
  # TODO: is there some better way to do it?
  return db.execute('SELECT id FROM games ORDER BY id DESC LIMIT 1;'
                    ).fetchone()['id']


def set_second_player_ip(
    db: sqlite3.Connection, link: str, second_player_ip: str
) -> bool:
  '''
  Sets value of `second_player_ip` field in entry with appropriate link. If
  there is no such a link in the database or `second_player_ip` is already
  set, returns False.
  '''
  result = db.execute(
      'SELECT id FROM games WHERE second_player_ip IS NULL AND link == ?',
      [link]
  ).fetchone()
  if result is None:
    return False
  db.execute(
      'UPDATE games SET second_player_ip = ? WHERE id == ?',
      [second_player_ip, result['id']]
  )
  db.commit()
  return True


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
