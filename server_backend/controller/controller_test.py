from server_backend.controller.controller import *


class TestContoller:
  def _get_db(self) -> sqlite3.Connection:
    DB_SETUP_SCRIPT_PATH = './flaskr/schema.sql'
    db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    with open(DB_SETUP_SCRIPT_PATH, 'r') as f:
      db.executescript(f.read())
    return db

  def test_load_script(self, tmp_path: pathlib.PosixPath):
    controller = Controller('', tmp_path)
    db = self._get_db()
    status, script_id = controller.load_script(db, 1, '')
    assert status
    assert isinstance(script_id, int)

  def test_create_game(self, tmp_path: pathlib.PosixPath):
    controller = Controller('', tmp_path)
    db = self._get_db()
    status, script_id = controller.load_script(db, 1, '')
    assert status
    assert isinstance(script_id, int)
    controller.create_game(db, 1, script_id)
