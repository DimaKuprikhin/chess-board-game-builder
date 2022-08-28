from executer.executer_utils import *
import pytest


class TestExecuterUtils:
  def _serialize_call_function_request_helper(self, script_id, function, args):
    serialized = serialize_call_function_request(script_id, function, args)
    script_id_, function_, args_ = deserialize_call_function_request(
        serialized
    )
    assert script_id_ == script_id
    assert function_ == function
    assert args_ == args

  def _serialize_load_script_request_helper(self, script_id, module_name):
    serialized = serialize_load_script_request(script_id, module_name)
    script_id_, module_name_ = deserialize_load_script_request(serialized)
    assert script_id_ == script_id
    assert module_name_ == module_name

  def _serialize_unload_script_request_helper(self, script_id):
    serialized = serialize_unload_script_request(script_id)
    script_id_ = deserialize_unload_script_request(serialized)
    assert script_id_ == script_id

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
    self._serialize_call_function_request_helper('script_id', 'func tion', [])
    self._serialize_call_function_request_helper(
        '3', '', ['str', 3, [{
            'a': 12
        }, True]]
    )
    self._serialize_call_function_request_helper(
        'another id', '.function()', ['hello world ', False]
    )
    with pytest.raises(TypeError):
      self._serialize_call_function_request_helper([], '5', [])
    with pytest.raises(TypeError):
      self._serialize_call_function_request_helper('id', 5, [])
    with pytest.raises(TypeError):
      self._serialize_call_function_request_helper('id', '5', {'a'})

  def test_serialize_load_script_request(self):
    self._serialize_load_script_request_helper('', '')
    self._serialize_load_script_request_helper('id', 'module_name')
    with pytest.raises(TypeError):
      self._serialize_load_script_request_helper(4, 'module_name')
    with pytest.raises(TypeError):
      self._serialize_load_script_request_helper('id', ['module_name'])

  def test_serialize_unload_script_request(self):
    self._serialize_unload_script_request_helper('')
    self._serialize_unload_script_request_helper('script_id')
    with pytest.raises(TypeError):
      self.test_serialize_unload_script_request({ 'script_id': 23 })

  def test_serialize_request(self):
    self._serialize_request_helper('', '')
    self._serialize_request_helper(
        'load_script',
        serialize_load_script_request('script_id', 'module_name')
    )
    self._serialize_request_helper(
        'unload_script', serialize_unload_script_request('script_id')
    )
    self._serialize_request_helper(
        'unload_script',
        serialize_call_function_request('script_id', 'function', ['args'])
    )
    with pytest.raises(TypeError):
      self._serialize_request_helper(123, 'data')
    with pytest.raises(TypeError):
      self._serialize_request_helper('load_script', ['data'])

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
