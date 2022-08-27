from executer.executer import Executer
from executer.executer_utils import serialize_function_call, deserialize_function_result


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


class TestExecuter:
  def test_empty_run(self):
    Executer().run(FakeInputIter([]))

  def test_run_input(self):
    Executer().run(FakeInputIter([serialize_function_call('getArray', [3])]))