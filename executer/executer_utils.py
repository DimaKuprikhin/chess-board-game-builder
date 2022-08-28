import json
from typing import Any, Tuple


def _check_type(obj, type):
  if not isinstance(obj, type):
    raise TypeError


def serialize_call_function_request(
    script_id: str, function: str, args: list
) -> str:
  '''
  Function call request contains of a name of the module(script), a name of the
  function, that we want to call, and a list of the arguments, that the
  function takes. Returns json string containing three keys: 'script',
  'function' and 'args'.
  '''
  _check_type(script_id, str)
  _check_type(function, str)
  _check_type(args, list)
  return json.dumps({
      'script_id': script_id,
      'function': function,
      'args': args
  })


def deserialize_call_function_request(
    serialized: str
) -> Tuple[str, str, list]:
  '''
  After deserializing, makes sure that deserialized script_id, function name
  and args have the correct types.
  '''
  deserialized = json.loads(serialized)
  script_id = deserialized['script_id']
  function = deserialized['function']
  args = deserialized['args']
  _check_type(script_id, str)
  _check_type(function, str)
  _check_type(args, list)
  return script_id, function, args


def serialize_load_script_request(script_id: str, module_name: str) -> str:
  _check_type(script_id, str)
  _check_type(module_name, str)
  return json.dumps({ 'script_id': script_id, 'module_name': module_name })


def deserialize_load_script_request(serialized: str) -> Tuple[str, str]:
  deserialized = json.loads(serialized)
  script_id = deserialized['script_id']
  module_name = deserialized['module_name']
  _check_type(script_id, str)
  _check_type(module_name, str)
  return script_id, module_name


def serialize_unload_script_request(script_id) -> str:
  return json.dumps({ 'script_id': script_id })


def deserialize_unload_script_request(serialized: str) -> str:
  deserialized = json.loads(serialized)
  script_id = deserialized['script_id']
  _check_type(script_id, str)
  return script_id


def serialize_request(request_type: str, request_data: str) -> str:
  _check_type(request_type, str)
  _check_type(request_data, str)
  return json.dumps({
      'request_type': request_type,
      'request_data': request_data
  })


def deserialize_request(serialized: str) -> Tuple[str, str]:
  deserialized = json.loads(serialized)
  request_type = deserialized['request_type']
  request_data = deserialized['request_data']
  _check_type(request_type, str)
  _check_type(request_data, str)
  return request_type, request_data


def serialize_response(status: bool, result: Any) -> str:
  _check_type(status, bool)
  return json.dumps({ 'status': status, 'result': result })


def deserialize_response(serialized: str) -> Tuple[bool, Any]:
  deserialized = json.loads(serialized)
  status = deserialized['status']
  result = deserialized['result']
  _check_type(status, bool)
  return status, result
