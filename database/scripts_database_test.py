import importlib
from database.scripts_database import *


class TestScriptsDatabase:
  def _get_db(self, tmp_path: pathlib.PosixPath):
    db = ScriptsDatabase(tmp_path, 'base')
    assert not db.contains(1)
    assert not db.remove_script(2)
    assert not db.get_module_name(3)
    return db

  def _add_script(self, db: ScriptsDatabase):
    script_id = db.add_script('')
    assert db.contains(script_id)
    assert isinstance(script_id, int)
    assert db.get_module_name(script_id)
    return script_id

  def _remove_script(self, db: ScriptsDatabase, script_id: int):
    assert db.remove_script(script_id)
    assert db.get_module_name(script_id) is None
    assert not db.contains(script_id)

  def test_create_db(self, tmp_path: pathlib.PosixPath):
    db = self._get_db(tmp_path)

  def test_add_remove_scripts(self, tmp_path: pathlib.PosixPath):
    db = self._get_db(tmp_path)
    first_id = self._add_script(db)
    second_id = self._add_script(db)
    assert first_id != second_id
    self._remove_script(db, second_id)
    assert db.contains(first_id)
    self._remove_script(db, first_id)
    assert db.contains(second_id)

  def test_import_by_module_name(self):
    db = ScriptsDatabase(
        pathlib.PosixPath('test_data', 'scripts_db_data'),
        'test_data.scripts_db_data'
    )
    script_id = db.add_script('')
    module_name = db.get_module_name(script_id)
    importlib.import_module(module_name)
    db.remove_script(script_id)
