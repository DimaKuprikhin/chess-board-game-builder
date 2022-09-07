import json
from typing import Any, Tuple


def check_type(obj, type):
  if not isinstance(obj, type):
    raise TypeError


def serialize_call_function_request(
    module_name: str, function: str, args: list, timeout: float
) -> str:
  '''
  Function call request contains of a name of the module, a name of the
  function, that we want to call, and a list of the arguments, that the
  function takes. Returns json string containing three keys: 'module_name',
  'function' and 'args'.
  '''
  check_type(module_name, str)
  check_type(function, str)
  check_type(args, list)
  check_type(timeout, float)
  return json.dumps({
      'module_name': module_name,
      'function': function,
      'args': args,
      'timeout': timeout
  })


def deserialize_call_function_request(
    serialized: str
) -> Tuple[str, str, list, float]:
  '''
  After deserializing, makes sure that deserialized module_name, function name
  and args have the correct types.
  '''
  deserialized = json.loads(serialized)
  module_name = deserialized['module_name']
  function = deserialized['function']
  args = deserialized['args']
  timeout = deserialized['timeout']
  check_type(module_name, str)
  check_type(function, str)
  check_type(args, list)
  check_type(timeout, float)
  return module_name, function, args, timeout


def serialize_request(request_type: str, request_data: str) -> str:
  check_type(request_type, str)
  check_type(request_data, str)
  return json.dumps({
      'request_type': request_type,
      'request_data': request_data
  })


def deserialize_request(serialized: str) -> Tuple[str, str]:
  deserialized = json.loads(serialized)
  request_type = deserialized['request_type']
  request_data = deserialized['request_data']
  check_type(request_type, str)
  check_type(request_data, str)
  return request_type, request_data


def serialize_response(status: bool, result: Any) -> str:
  check_type(status, bool)
  return json.dumps({ 'status': status, 'result': result })


def deserialize_response(serialized: str) -> Tuple[bool, Any]:
  deserialized = json.loads(serialized)
  status = deserialized['status']
  result = deserialized['result']
  check_type(status, bool)
  return status, result
