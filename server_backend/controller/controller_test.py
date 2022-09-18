from server_backend.controller.controller import *
from server_backend.database.game_dto import GameDTO


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
    status, script_id = controller.load_script(db, '')
    assert status
    assert isinstance(script_id, int)

  def test_create_game(self, tmp_path: pathlib.PosixPath):
    controller = Controller('', tmp_path)
    db = self._get_db()
    status, script_id = controller.load_script(db, '')
    assert status
    assert isinstance(script_id, int)
    game = GameDTO(
        first_player_id='1',
        first_player_plays_as='white',
        move_number=0,
        turn='white',
        script_id=script_id
    )
    status, result = controller.create_game(db, game)
    assert status
    assert isinstance(result.get_id(), int)
    assert isinstance(result.get_link(), str)

  def test_join_by_link(self):
    controller = Controller(
        'server_backend.test_data.scripts_dir',
        pathlib.PosixPath('.', 'server_backend', 'test_data', 'scripts_dir'),
        True
    )
    db = self._get_db()
    script = 'def get_starting_state():\n'
    script += '  return 3'
    status, script_id = controller.load_script(db, script)
    assert status
    game = GameDTO(
        first_player_id=1,
        first_player_plays_as='white',
        move_number=0,
        turn='white',
        script_id=script_id
    )
    status, result = controller.create_game(db, game)
    assert status
    link = result.get_link()
    status, result = controller.join_by_link(db, link, 2)
    assert status
    assert result['game_state'] == 3
    assert result['color'] == 'black'
    assert result['turn'] == 'white'
    assert isinstance(result['game_id'], int)
    status, result = controller.join_by_link(db, link, 2)
    assert not status
    status, result = controller.join_by_link(db, 'link', 2)
    assert not status

  def test_make_move_and_get_game_state(self):
    script = 'def get_starting_state():\n'
    script += '  return {"pieces":[{"name": "dummy", "color": "white", "x": 0, "y": 0}],\n'
    script += '          "possible_moves":[{"from_x":0, "from_y": 0, "to_x": 0, "to_y": 1}],\n'
    script += '          "additional_data":{}, "status":"running"}\n\n'
    script += 'def make_move(pieces, move, next_turn, additional_data):\n'
    script += '  return {"pieces":[{"name": "dummy", "color": "white", "x": 0, "y": 1}],\n'
    script += '          "possible_moves":[], "additional_data":{}, "status":"running"}\n\n'

    controller = Controller(
        'server_backend.test_data.scripts_dir',
        pathlib.PosixPath('.', 'server_backend', 'test_data', 'scripts_dir'),
        True
    )
    db = self._get_db()
    status, script_id = controller.load_script(db, script)
    assert status

    game = GameDTO(
        first_player_id=1,
        first_player_plays_as='white',
        move_number=0,
        turn='white',
        script_id=script_id
    )
    status, result = controller.create_game(db, game)
    assert status
    link = result.get_link()

    status, result = controller.join_by_link(db, link, 2)
    assert status
    game_id = result['game_id']
    move = { 'from_x': 0, 'from_y': 0, 'to_x': 0, 'to_y': 1 }

    status, result = controller.make_move(db, game_id, 1, move)
    assert status
    game_state = result['game_state']
    assert result['color'] == 'white'
    assert result['turn'] == 'black'
    assert game_state['pieces'] == [{
        'name': 'dummy',
        'color': 'white',
        'x': 0,
        'y': 1
    }]
    assert game_state['possible_moves'] == []
    assert game_state['additional_data'] == {}
    assert game_state['status'] == 'running'

    status, result = controller.get_game_state(db, game_id, 2)
    assert status
    assert result['color'] == 'black'
    assert result['turn'] == 'black'
    game_state = result['game_state']
    assert game_state['pieces'] == [{
        'name': 'dummy',
        'color': 'white',
        'x': 0,
        'y': 1
    }]
    assert game_state['possible_moves'] == []
    assert game_state['additional_data'] == {}
    assert game_state['status'] == 'running'
