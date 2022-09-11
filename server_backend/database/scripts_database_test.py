import importlib
from typing import Tuple
from server_backend.database.scripts_database import *


class TestScriptsDatabase:
  def _get_db(self) -> sqlite3.Connection:
    DB_SETUP_SCRIPT_PATH = './flaskr/schema.sql'
    db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    with open(DB_SETUP_SCRIPT_PATH, 'r') as f:
      db.executescript(f.read())
    return db

  def _add_script(
      self, db: sqlite3.Connection, user_id: int, base_module_name: str,
      scripts_dir: pathlib.PosixPath
  ) -> int:
    script_id = add_script(db, user_id, '', base_module_name, scripts_dir)
    assert contains(db, script_id)
    assert isinstance(script_id, int)
    assert get_module_name(db, script_id)
    return script_id

  def _remove_script(self, db: sqlite3.Connection, script_id: int):
    script_path = get_script_path(db, script_id)
    assert os.path.exists(script_path.absolute())
    assert remove_script(db, script_id)
    assert get_module_name(db, script_id) is None
    assert get_script_path(db, script_id) is None
    assert not os.path.exists(script_path.absolute())
    assert not contains(db, script_id)

  def test_create_db(self):
    db = self._get_db()
    db.execute('SELECT 1;')

  def test_add_remove_scripts(self, tmp_path: pathlib.PosixPath):
    db = self._get_db()
    base_module_name = 'scripts'
    first_id = self._add_script(db, 1, base_module_name, tmp_path)
    second_id = self._add_script(db, 1, base_module_name, tmp_path)
    assert first_id != second_id
    self._remove_script(db, second_id)
    assert contains(db, first_id)
    self._remove_script(db, first_id)

  def test_import_by_module_name(self):
    base_module_name = 'server_backend.test_data.scripts_dir'
    scripts_dir = pathlib.PosixPath(
        '.', 'server_backend', 'test_data', 'scripts_dir'
    )
    if not os.path.isdir(scripts_dir):
      os.mkdir(scripts_dir)
    db = self._get_db()
    script_id = add_script(db, 1, 'print(1)', base_module_name, scripts_dir)
    module_name = get_module_name(db, script_id)
    importlib.import_module(module_name)
    self._remove_script(db, script_id)
