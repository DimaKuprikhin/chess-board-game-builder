from executer.executer_utils import *
import pytest


class TestExecuterUtils:
  def _serialize_function_call_helper(self, function, args):
    serialized = serialize_function_call(function, args)
    function_, args_ = deserialize_function_call(serialized)
    assert function_ == function
    assert args_ == args

  def _serialize_function_result_helper(self, result):
    serialized = serialized_function_result(result)
    result_ = deserialize_function_result(serialized)
    assert result_ == result

  def test_serialize_function_call(self):
    self._serialize_function_call_helper('', [])
    self._serialize_function_call_helper('func tion', [])
    self._serialize_function_call_helper('', ['str', 3, [{ 'a': 12 }, True]])
    self._serialize_function_call_helper(
        '.function()', ['hello world ', False]
    )
    with pytest.raises(TypeError):
      self._serialize_function_call_helper(5, [])
    with pytest.raises(TypeError):
      self._serialize_function_call_helper('5', {'a'})

  def test_serialize_function_result(self):
    self._serialize_function_result_helper('')
    self._serialize_function_result_helper('function result')
    self._serialize_function_result_helper(['func', 'result'])
    self._serialize_function_result_helper(5)
    self._serialize_function_result_helper({
        'result': 123,
        'is_valid': [False, False, True]
    })
