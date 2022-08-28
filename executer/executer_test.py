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


class TestExecuter:
  def test_empty_run(self):
    Executer().run(FakeInputIter([]), FakeOutput())

  def test_call_function(self):
    requests = []
    request_data = serialize_call_function_request(
        'executer.script', 'getArray', [4]
    )
    requests.append(serialize_request('call_function', request_data))
    request_data = serialize_call_function_request(
        'executer.script', 'getMap', ['key', 123]
    )
    requests.append(serialize_request('call_function', request_data))
    request_data = serialize_call_function_request(
        'executer.script', 'getSquare', [6]
    )
    requests.append(serialize_request('call_function', request_data))

    output = FakeOutput()
    Executer().run(FakeInputIter(requests), output)
    expected_output = '{"status": true, "result": [0, 1, 2, 3]}\n'
    expected_output += '{"status": true, "result": {"key": 123}}\n'
    expected_output += '{"status": true, "result": 36}\n'
    assert output.get_data() == expected_output
