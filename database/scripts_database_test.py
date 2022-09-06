import importlib
from database.scripts_database import *


class TestScriptsDatabase:
  def _get_db(self, tmp_path):
    db = ScriptsDatabase(tmp_path, 'base')
    assert not db.remove_script(1)
    assert not db.get_module_name(1)
    return db

  def _add_script(self, db):
    script_id = db.add_script('')
    assert isinstance(script_id, int)
    assert db.get_module_name(script_id)
    return script_id

  def _remove_script(self, db, script_id):
    assert db.remove_script(script_id)
    assert db.get_module_name(script_id) is None

  def test_create_db(self, tmp_path):
    db = self._get_db(tmp_path)

  def test_add_remove_scripts(self, tmp_path):
    db = self._get_db(tmp_path)
    first_id = self._add_script(db)
    second_id = self._add_script(db)
    assert first_id != second_id
    self._remove_script(db, second_id)
    assert db.get_module_name(first_id)
    self._remove_script(db, first_id)
    assert not db.get_module_name(second_id)

  def test_import_by_module_name(self):
    db = ScriptsDatabase(pathlib.PosixPath('test_data', 'scripts_db_data'), 'test_data.scripts_db_data')
    script_id = db.add_script('')
    module_name = db.get_module_name(script_id)
    importlib.import_module(module_name)
    db.remove_script(script_id)
