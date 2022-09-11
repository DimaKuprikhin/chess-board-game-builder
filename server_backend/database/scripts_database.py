import os
import pathlib
import random
import string
import sqlite3


def _generate_unique_string(n: int) -> str:
  return ''.join(
      random.choice(string.ascii_letters + string.digits) for _ in range(n)
  )


def add_script(
    db: sqlite3.Connection, user_id: int, script: str, base_module_name: str,
    scripts_dir: pathlib.PosixPath
) -> int:
  '''
  Adds user script to scripts table, creates a unique module name and
  a file in `scripts_dir`. On success, returns script id of the added script.
  '''
  script_name = _generate_unique_string(3)
  module_name = base_module_name + '.' + script_name
  script_path = scripts_dir.joinpath(script_name + '.py').as_posix()
  db.execute(
      'INSERT INTO scripts (user_id, module_name, script_path) VALUES (?, ?, ?);',
      [user_id, module_name, script_path]
  )
  db.commit()
  # TODO: is there some better way to do it?
  script_id = db.execute(
      'SELECT id FROM scripts ORDER BY id DESC LIMIT 1;', []
  ).fetchone()['id']
  with open(script_path, 'w') as f:
    f.write(script)
  return script_id


def contains(db: sqlite3.Connection, script_id: int) -> bool:
  '''
  Returns True, if the database contains an entry with the given script id.
  '''
  return db.execute('SELECT id FROM scripts WHERE id == ?;',
                    [script_id]).fetchone() is not None


def get_module_name(db: sqlite3.Connection, script_id: int) -> str:
  '''
  Returns a unique scripts module name, which can be imported in other
  modules. Returns None, if there is no script with the given script id in
  database.
  '''
  result = db.execute(
      'SELECT module_name FROM scripts WHERE id == ?;', [script_id]
  ).fetchone()
  return None if result is None else result['module_name']


def get_script_path(
    db: sqlite3.Connection, script_id: int
) -> pathlib.PosixPath:
  '''
  Returns a unique script path of the script with the given script id.
  '''
  result = db.execute(
      'SELECT script_path FROM scripts WHERE id == ?;', [script_id]
  ).fetchone()
  return None if result is None else pathlib.PosixPath(result['script_path'])


def remove_script(db: sqlite3.Connection, script_id: int) -> bool:
  '''
  Removes a script entry from the database and corresponding script file.
  On success, returns True. If database didn't contain this script id, returns
  False.
  '''
  script_path = db.execute(
      'SELECT script_path FROM scripts WHERE id == ?;', [script_id]
  ).fetchone()
  if script_path is None:
    return False
  db.execute('DELETE FROM scripts WHERE id == ?;', [script_id])
  db.commit()
  os.remove(script_path['script_path'])
  return True
