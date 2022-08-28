from executer.executer_utils import *
import pytest


class TestExecuterUtils:
  def _serialize_call_function_request_helper(
      self, module_name, function, args
  ):
    serialized = serialize_call_function_request(module_name, function, args)
    module_name_, function_, args_ = deserialize_call_function_request(
        serialized
    )
    assert module_name_ == module_name
    assert function_ == function
    assert args_ == args

  def _serialize_request_helper(self, type, data):
    serialized = serialize_request(type, data)
    type_, data_ = deserialize_request(serialized)
    assert type_ == type
    assert data_ == data

  def _serialize_response_helper(self, status, response):
    serialized = serialize_response(status, response)
    status_, response_ = deserialize_response(serialized)
    assert status_ == status
    assert response_ == response

  def test_serialize_call_function_request(self):
    self._serialize_call_function_request_helper('', '', [])
    self._serialize_call_function_request_helper(
        'module_name', 'func tion', []
    )
    self._serialize_call_function_request_helper(
        '3', '', ['str', 3, [{
            'a': 12
        }, True]]
    )
    self._serialize_call_function_request_helper(
        'another module', '.function()', ['hello world ', False]
    )
    with pytest.raises(TypeError):
      self._serialize_call_function_request_helper([], '5', [])
    with pytest.raises(TypeError):
      self._serialize_call_function_request_helper('module', 5, [])
    with pytest.raises(TypeError):
      self._serialize_call_function_request_helper('module', '5', {'a'})

  def test_serialize_request(self):
    self._serialize_request_helper('', '')
    self._serialize_request_helper(
        'call_function',
        serialize_call_function_request('module name', 'function', ['args'])
    )
    with pytest.raises(TypeError):
      self._serialize_request_helper(123, 'data')
    with pytest.raises(TypeError):
      self._serialize_request_helper('call_function', ['data'])

  def test_serialize_response(self):
    self._serialize_response_helper(True, '')
    self._serialize_response_helper(False, 'function result')
    self._serialize_response_helper(True, ['func', 'result'])
    self._serialize_response_helper(False, 5)
    self._serialize_response_helper(
        True, {
            'result': 123,
            'is_valid': [False, False, True]
        }
    )
    with pytest.raises(TypeError):
      self._serialize_response_helper('OK', 'result')
