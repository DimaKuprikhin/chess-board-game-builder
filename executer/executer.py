import importlib
from typing import Any, Tuple
from executer import executer_utils


class Executer:
  def __init__(self):
    self.scripts = {}

  def _call_function(self, module_name: str, function: str,
                     args: list) -> Tuple[bool, Any]:
    '''
    Imports module `module_name` and calls function in this module with the
    given arguments. On success, returns True status and result of the
    function. Otherwise, returns False and a failure description string.
    '''
    try:
      module = importlib.import_module(module_name)
      func = getattr(module, function)
      result = func(*args)
      return True, result
    except ModuleNotFoundError as ex:
      # Missing module_name.
      return False, 'Module not found'
    except AttributeError as ex:
      # Missing function.
      return False, 'Function not found'
    except TypeError as ex:
      # Wrong number or types of arguments.
      return False, 'Wrong arguments'
    except Exception as ex:
      return False, 'Unknown error'

  def _handle_request(self, request: str) -> Tuple[bool, Any]:
    '''
    Parses received requests and calls appropriate methods.
    '''
    # By now, we need to handle only call_function request type.
    request_type, request_data = executer_utils.deserialize_request(request)
    if request_type == 'call_function':
      module_name, function, args = executer_utils.deserialize_call_function_request(
          request_data
      )
      return self._call_function(module_name, function, args)
    else:
      return False, 'Unknown request type'

  def run(self, input_iter, output):
    '''
    Runs an infinite loop in which Executer receives requests from the
    ExecuterManager from the main process and sends responses.
    '''
    for request in input_iter:
      request = request.strip()
      status, result = self._handle_request(request)
      response = executer_utils.serialize_response(status, result)
      output.write(response + '\n')
