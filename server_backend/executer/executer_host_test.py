from server_backend.executer.executer_host import ExecuterHost


class TestExecuterHost:
  def _create_executer_host_helper(self):
    host = ExecuterHost(True)
    assert not host.is_alive()
    assert not host.has_executer()
    return host

  def _create_executer_helper(self, host):
    assert not host.is_alive()
    assert not host.has_executer()
    assert host.create_executer()
    assert host.is_alive()
    assert host.has_executer()

  def _call_function_helper(
      self,
      host,
      module,
      function,
      args,
      expected_status,
      expected_result,
      timeout=0.1
  ):
    status, result = host.call_script_function(module, function, args, timeout)
    assert expected_status == status
    assert expected_result == result

  def test_create_executer(self):
    host = self._create_executer_host_helper()
    self._create_executer_helper(host)

  def test_call_function_without_executer(self):
    host = self._create_executer_host_helper()
    self._call_function_helper(
        host, 'server_backend.test_data.functions', 'get_array', [1], False,
        'Executer hasn\'t been created'
    )

  def test_call_function(self):
    module = 'server_backend.test_data.functions'
    host = self._create_executer_host_helper()
    self._create_executer_helper(host)
    self._call_function_helper(
        host, module, 'get_array', [5], True, [0, 1, 2, 3, 4]
    )
    self._call_function_helper(
        host, module, 'get_map', ['key', {
            'value': 123
        }], True, { 'key': {
            'value': 123
        } }
    )
    self._call_function_helper(host, module, 'get_square', [12], True, 144)

  def test_script_exception(self):
    host = ExecuterHost(True)
    host.create_executer()
    module = 'server_backend.test_data.exception_thrower'
    function = 'throw_ex'
    args = ['message for exception']
    status, result = host.call_script_function(module, function, args, 0.1)
    assert not status
    assert result == 'Exception in script: message for exception'

  def test_infinite_loop(self):
    host = self._create_executer_host_helper()
    self._create_executer_helper(host)
    self._call_function_helper(
        host, 'server_backend.test_data.infinite_loop', 'run_infinite_loop', [], False,
        'Function timed out'
    )

  def test_heavy_function(self):
    host = self._create_executer_host_helper()
    self._create_executer_helper(host)
    module = 'server_backend.test_data.heavy_functions'
    self._call_function_helper(
        host, module, 'heavy_function', [], False, 'Function timed out'
    )
    self._call_function_helper(
        host, module, 'heavy_power', [], False, 'Function timed out'
    )

  def test_memory_limit(self):
    host = self._create_executer_host_helper()
    self._create_executer_helper(host)
    module = 'server_backend.test_data.memory_users'
    self._call_function_helper(host, module, 'good_memory_user', [], True, 0)
    self._call_function_helper(
        host, module, 'bad_memory_user', [], False, 'Memory limit exceeded'
    )
