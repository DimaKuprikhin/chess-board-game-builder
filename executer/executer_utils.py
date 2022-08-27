import json
from typing import Tuple


def serialize_function_call(function: str, args: list) -> str:
  '''
  Function call contains of a name of the function, that we want to call, and
  a list of the arguments, that the function takes. Returns json string
  containing two keys: 'function' and 'args'.
  '''
  if (not isinstance(function, type(''))) or (not isinstance(args, type([]))):
    raise TypeError
  return json.dumps({ 'function': function, 'args': args })


def deserialize_function_call(serialized: str) -> Tuple[str, list]:
  '''
  After deserializing, makes sure that deserialized function name and args
  are string and list respectively.
  '''
  deserialized = json.loads(serialized)
  function = deserialized['function']
  args = deserialized['args']
  if (not isinstance(function, type(''))) or (not isinstance(args, type([]))):
    raise TypeError
  return function, args


def serialized_function_result(result) -> str:
  return json.dumps({ 'result': result })


def deserialize_function_result(serialized: str):
  return json.loads(serialized)['result']
