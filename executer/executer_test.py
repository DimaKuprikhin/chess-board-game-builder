import time
from executer.executer import Executer
from executer.executer_utils import *


class FakeInputIter:
  def __init__(self, lines):
    self.lines = lines
    self.cur_line_index = 0

  def __iter__(self):
    return self

  def __next__(self):
    if self.cur_line_index < len(self.lines):
      self.cur_line_index += 1
      return self.lines[self.cur_line_index - 1]
    raise StopIteration


class FakeOutput:
  def __init__(self):
    self.data = ''

  def write(self, data: str):
    self.data += data

  def flush(self):
    return

  def get_data(self) -> str:
    return self.data


def _serialize_function_call_request_helper(
    module_name: str, function: str, args: list, timeout: float
) -> str:
  request_data = serialize_call_function_request(
      module_name, function, args, timeout
  )
  return serialize_request('call_function', request_data)


class TestExecuter:
  def test_empty_run(self):
    Executer(True).run(FakeInputIter([]), FakeOutput())

  def test_call_function(self):
    module = 'test_data.functions'
    requests = [
        _serialize_function_call_request_helper(module, 'get_array', [4], 0.0),
        _serialize_function_call_request_helper(
            module, 'get_map', ['key', 123], 0.0
        ),
        _serialize_function_call_request_helper(
            module, 'get_square', [6], 0.0
        )
    ]
    output = FakeOutput()
    Executer(True).run(FakeInputIter(requests), output)
    expected_output = '{"status": true, "result": [0, 1, 2, 3]}\n'
    expected_output += '{"status": true, "result": {"key": 123}}\n'
    expected_output += '{"status": true, "result": 36}\n'
    assert output.get_data() == expected_output

  def test_missing_module(self):
    module = 'test_data.missing_scirpt'
    requests = [
        _serialize_function_call_request_helper(module, 'func', [], 0.0)
    ]
    output = FakeOutput()
    Executer(True).run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Module not found"}\n'
    assert output.get_data() == expected_output

  def test_missing_function(self):
    module = 'test_data.functions'
    requests = [
        _serialize_function_call_request_helper(
            module, 'missing_func', [], 0.0
        )
    ]
    output = FakeOutput()
    Executer(True).run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Function not found"}\n'
    assert output.get_data() == expected_output

  def test_wrong_arguments(self):
    module = 'test_data.functions'
    requests = [
        _serialize_function_call_request_helper(
            module, 'get_array', [1, 2], 0.0
        )
    ]
    output = FakeOutput()
    Executer(True).run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Wrong arguments"}\n'
    assert output.get_data() == expected_output

    requests = [
        _serialize_function_call_request_helper(
            module, 'get_array', ['1'], 0.0
        )
    ]
    output = FakeOutput()
    Executer(True).run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Wrong arguments"}\n'
    assert output.get_data() == expected_output

  def test_exception_throw_by_script(self):
    requests = [
        _serialize_function_call_request_helper(
            'test_data.exception_thrower', 'throw_ex',
            ['exception from script function'], 0.1
        )
    ]
    output = FakeOutput()
    Executer(True).run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Exception in script: exception from script function"}\n'
    assert output.get_data() == expected_output

  def test_infinite_loop(self):
    timeout = 0.1
    requests = [
        _serialize_function_call_request_helper(
            'test_data.infinite_loop', 'run_infinite_loop', [], timeout
        )
    ]
    output = FakeOutput()
    start = time.time()
    Executer(True).run(FakeInputIter(requests), output)
    end = time.time()
    expected_output = '{"status": false, "result": "Function timed out"}\n'
    assert output.get_data() == expected_output
    assert (end - start) < 1.1 * timeout

  def test_heavy_function(self):
    timeout = 0.1
    requests = [
        _serialize_function_call_request_helper(
            'test_data.heavy_functions', 'heavy_function', [], timeout
        )
    ]
    output = FakeOutput()
    start = time.time()
    Executer(True).run(FakeInputIter(requests), output)
    end = time.time()
    expected_output = '{"status": false, "result": "Function timed out"}\n'
    assert output.get_data() == expected_output
    assert (end - start) < 1.1 * timeout

    requests = [
        _serialize_function_call_request_helper(
            'test_data.heavy_functions', 'heavy_power', [], timeout
        )
    ]
    output = FakeOutput()
    start = time.time()
    Executer(True).run(FakeInputIter(requests), output)
    end = time.time()
    expected_output = '{"status": false, "result": "Function timed out"}\n'
    assert output.get_data() == expected_output
    assert (end - start) < 1.1 * timeout

  def test_memory_limit(self):
    requests = [
        _serialize_function_call_request_helper(
            'test_data.memory_users', 'good_memory_user', [], 0.1
        )
    ]
    output = FakeOutput()
    Executer(True).run(FakeInputIter(requests), output)
    expected_output = '{"status": true, "result": 0}\n'
    assert output.get_data() == expected_output

    requests = [
        _serialize_function_call_request_helper(
            'test_data.memory_users', 'bad_memory_user', [], 0.1
        )
    ]
    output = FakeOutput()
    Executer(True).run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Memory limit exceeded"}\n'
    assert output.get_data() == expected_output
