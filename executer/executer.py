import importlib
from typing import Any, Tuple
from executer import executer_utils


class Executer:
  def __init__(self):
    self.scripts = {}

  def call_function(self, module_name: str, function: str,
                    args: list) -> Tuple[bool, Any]:
    try:
      module = importlib.import_module(module_name)
      func = getattr(module, function)
      result = func(*args)
      return True, result
    except Exception as ex:
      return False, ex

  def _handle_request(self, request: str) -> Tuple[bool, Any]:
    request_type, request_data = executer_utils.deserialize_request(request)
    if request_type == 'call_function':
      module_name, function, args = executer_utils.deserialize_call_function_request(
          request_data
      )
      return self.call_function(module_name, function, args)
    else:
      return False, 'Unknown request type'

  def run(self, input_iter, output):
    '''
    Runs an infinite loop in which Executer receives requests from the
    ExecuterManager from the main process and sends responces.
    '''
    for request in input_iter:
      request = request.strip()
      status, result = self._handle_request(request)
      print(status, result)
      response = executer_utils.serialize_response(status, result)
      output.write(response + '\n')
