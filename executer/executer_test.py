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

  def test_load_script(self):
    request_data = serialize_load_script_request('script', 'executer.script')
    request = serialize_request('load_script', request_data)
    output = FakeOutput()
    Executer().run(FakeInputIter([request]), output)
    assert output.get_data() == '{"status": true, "result": "OK"}\n'

  def test_call_function(self):
    request_data = serialize_load_script_request('script', 'executer.script')
    request = serialize_request('load_script', request_data)
    requests = [request]
    request_data = serialize_call_function_request('script', 'getArray', [3])
    request = serialize_request('call_function', request_data)
    requests.append(request)

    output = FakeOutput()
    Executer().run(FakeInputIter(requests), output)
    assert output.get_data() == '{"status": true, "result": "OK"}\n{"status": true, "result": [0, 1, 2]}\n'
