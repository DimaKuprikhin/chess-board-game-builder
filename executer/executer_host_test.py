from executer.executer_host import ExecuterHost


class TestExecuterHost:
  def test_create_executer(self):
    manager = ExecuterHost()
    assert not manager.is_alive('1')
    assert not manager.is_any_alive()
    manager.create_executer('1')
    assert manager.is_alive('1')
    assert manager.is_any_alive()

  def test_wrong_executer_id(self):
    manager = ExecuterHost()
    manager.create_executer('2')
    status, result = manager.call_script_function('1', '', '', [], 0.0)
    assert not status
    assert result == 'There is no executer with id 1'

  def test_call_function(self):
    executer_id = '1'
    module = 'test_data.script'
    timeout = 0.1
    manager = ExecuterHost(True)
    manager.create_executer(executer_id)
    status, result = manager.call_script_function(
        executer_id, module, 'getArray', [5], timeout
    )
    assert status
    expected_result = [0, 1, 2, 3, 4]
    assert result == expected_result

    status, result = manager.call_script_function(
        executer_id, module, 'getMap', ['key', {
            'value': 123
        }], timeout
    )
    assert status
    expected_result = { 'key': { 'value': 123 } }
    assert result == expected_result

    status, result = manager.call_script_function(
        executer_id, module, 'getSquare', [12], timeout
    )
    assert status
    assert result == 144

  def test_script_exception(self):
    manager = ExecuterHost(True)
    manager.create_executer('1')
    module = 'test_data.exception_thrower'
    function = 'function_that_throws_ex'
    args = ['message for exception']
    status, result = manager.call_script_function(
        '1', module, function, args, 0.1
    )
    assert not status
    assert result == 'Exception in script: message for exception'

  def test_infinite_loop(self):
    manager = ExecuterHost(True)
    manager.create_executer('1')
    module = 'test_data.infinite_loop'
    function = 'run_infinite_loop'
    status, result = manager.call_script_function(
        '1', module, function, [], 0.1
    )
    assert not status
    assert result == 'Function timed out'

  def test_heavy_function(self):
    manager = ExecuterHost(True)
    manager.create_executer('1')
    module = 'test_data.heavy_function'
    function = 'run_heavy_function'
    timeout = 0.1

    status, result = manager.call_script_function(
        '1', module, function, [], timeout
    )
    assert not status
    assert result == 'Function timed out'

    function = 'heavy_power'
    status, result = manager.call_script_function(
        '1', module, function, [], timeout
    )
    assert not status
    assert result == 'Function timed out'

  def test_memory_limit(self):
    manager = ExecuterHost(True)
    manager.create_executer('1')
    module = 'test_data.memory_user'
    function = 'good_memory_user'
    timeout = 0.1

    status, result = manager.call_script_function(
        '1', module, function, [], timeout
    )
    assert status
    assert result == 0

    function = 'bad_memory_user'
    status, result = manager.call_script_function(
        '1', module, function, [], timeout
    )
    assert not status
    assert result == 'Memory limit exceeded'
