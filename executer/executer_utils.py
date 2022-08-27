import json


def serialize_function_call(function, args):
  if (not isinstance(function, type(''))) or (not isinstance(args, type([]))):
    raise TypeError
  return json.dumps({ 'function': function, 'args': args })


def deserialize_function_call(serialized):
  deserialized = json.loads(serialized)
  function = deserialized['function']
  args = deserialized['args']
  if (not isinstance(function, type(''))) or (not isinstance(args, type([]))):
    raise TypeError
  return function, args


def serialized_function_result(result):
  return json.dumps({ 'result': result })


def deserialize_function_result(serialized):
  return json.loads(serialized)['result']
