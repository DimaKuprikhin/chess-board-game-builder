from server_backend.controller.controller import *
import pytest


class TestContoller:
  def test_init_dbs_multiple_times(self, tmp_path: pathlib.PosixPath):
    controller = Controller()
    controller.init_games_database()
    with pytest.raises(AssertionError):
      controller.init_games_database()
    with pytest.raises(AssertionError):
      controller.init_games_database()

    controller.init_scripts_database(tmp_path)
    with pytest.raises(AssertionError):
      controller.init_scripts_database(tmp_path)
    with pytest.raises(AssertionError):
      controller.init_scripts_database(tmp_path)

  def test_load_script(self, tmp_path: pathlib.PosixPath):
    controller = Controller()
    controller.init_scripts_database(tmp_path)
    assert controller.load_script('')[0]

  def test_load_script_without_init_db(self):
    controller = Controller()
    with pytest.raises(AssertionError):
      controller.load_script('')

  def test_create_game(self, tmp_path: pathlib.PosixPath):
    controller = Controller()
    controller.init_games_database()
    controller.init_scripts_database(tmp_path)
    status, script_id = controller.load_script('')
    assert status
    controller.create_game(1, script_id, '')

    status, script_id = controller.load_script('')
    assert status
    controller.create_game(2, script_id, '')

  def test_create_game_without_init_dbs(self, tmp_path: pathlib.PosixPath):
    controller = Controller()
    with pytest.raises(AssertionError):
      controller.create_game(0, 100, '')

    controller = Controller()
    controller.init_scripts_database(tmp_path)
    with pytest.raises(AssertionError):
      controller.create_game(1, 101, '')

    controller = Controller()
    controller.init_games_database()
    with pytest.raises(AssertionError):
      controller.create_game(2, 102, '')

  def test_create_game_with_invalid_script_id(
      self, tmp_path: pathlib.PosixPath
  ):
    controller = Controller()
    controller.init_games_database()
    controller.init_scripts_database(tmp_path)
    status, message = controller.create_game(1, 101, '')
    assert not status
    assert message == 'Can\'t create a game with incorrect script id'

  def test_create_multiple_games_with_same_user_id(
      self, tmp_path: pathlib.PosixPath
  ):
    controller = Controller()
    controller.init_games_database()
    controller.init_scripts_database(tmp_path)
    status, script_id = controller.load_script('')
    assert status
    status, message = controller.create_game(1, script_id, '')
    assert status
    status, message = controller.create_game(1, script_id, '')
    assert not status
    assert message == 'The same user can\'t create multiple games at the same time'
