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

  def get_data(self) -> str:
    return self.data


def _serialize_function_call_request_helper(
    module_name: str, function: str, args: list
) -> str:
  request_data = serialize_call_function_request(module_name, function, args)
  return serialize_request('call_function', request_data)


class TestExecuter:
  def test_empty_run(self):
    Executer().run(FakeInputIter([]), FakeOutput())

  def test_call_function(self):
    module = 'test_data.script'
    requests = [
        _serialize_function_call_request_helper(module, 'getArray', [4]),
        _serialize_function_call_request_helper(
            module, 'getMap', ['key', 123]
        ),
        _serialize_function_call_request_helper(module, 'getSquare', [6])
    ]
    output = FakeOutput()
    Executer().run(FakeInputIter(requests), output)
    expected_output = '{"status": true, "result": [0, 1, 2, 3]}\n'
    expected_output += '{"status": true, "result": {"key": 123}}\n'
    expected_output += '{"status": true, "result": 36}\n'
    assert output.get_data() == expected_output

  def test_missing_module(self):
    module = 'test_data.missing_scirpt'
    requests = [_serialize_function_call_request_helper(module, 'func', [])]
    output = FakeOutput()
    Executer().run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Module not found"}\n'
    assert output.get_data() == expected_output

  def test_missing_function(self):
    module = 'test_data.script'
    requests = [
        _serialize_function_call_request_helper(module, 'missing_func', [])
    ]
    output = FakeOutput()
    Executer().run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Function not found"}\n'
    assert output.get_data() == expected_output

  def test_wrong_arguments(self):
    module = 'test_data.script'
    requests = [
        _serialize_function_call_request_helper(module, 'getArray', [1, 2])
    ]
    output = FakeOutput()
    Executer().run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Wrong arguments"}\n'
    assert output.get_data() == expected_output

    requests = [
        _serialize_function_call_request_helper(module, 'getArray', ['1'])
    ]
    output = FakeOutput()
    Executer().run(FakeInputIter(requests), output)
    expected_output = '{"status": false, "result": "Wrong arguments"}\n'
    assert output.get_data() == expected_output
