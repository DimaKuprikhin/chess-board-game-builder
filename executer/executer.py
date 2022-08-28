import importlib
from common.logger import LogLevel, LOG
from executer import executer_utils


class Executer:
  def __init__(self):
    self.scripts = {}

  def call_function(self, script_id, function, *args):
    try:
      return True, getattr(self.scripts[script_id], function)(*args)
    except Exception as ex:
      return False, ex

  def load_script(self, script_id: str, module_name: str) -> bool:
    '''
    Imports a module by the given `module_name`. On success, returns True and
    stores the imported module. On any failure returns False.
    '''
    if script_id in self.scripts:
      return False, 'Executer already contains a script with script_id ' + str(
          script_id
      )
    try:
      module = importlib.import_module(module_name)
      self.scripts[script_id] = module
      return True, 'OK'
    except Exception as ex:
      return False, ex

  def unload_script(self, script_id):
    '''
    Unloads previously imported module. Actually, now we don't really unload
    anything, just remove an entry with unloaded module.
    '''
    if script_id in self.scripts:
      self.scripts.pop(script_id)
      return True, 'Script has been unload successfully'
    return False, 'Executer doesn\'t have a script with script_id ' + str(
        script_id
    )

  def _handle_request(self, request):
    request_type, request_data = executer_utils.deserialize_request(request)
    if request_type == 'load_script':
      script_id, module_name = executer_utils.deserialize_load_script_request(
          request_data
      )
      return self.load_script(script_id, module_name)
    elif request_type == 'unload_script':
      script_id = executer_utils.deserialize_unload_script_request(
          request_data
      )
      return self.unload_script(script_id)
    elif request_type == 'call_function':
      script_id, function, args = executer_utils.deserialize_call_function_request(
          request_data
      )
      return self.call_function(script_id, function, *args)
    else:
      return False, 'Unknown request type'

  def run(self, input_iter, output):
    '''
    Runs an infinite loop in which Executer receives requests from the
    ExecuterManager from the main process and sends responces.
    '''
    LOG(LogLevel.INFO, 'executer has been started')
    for request in input_iter:
      request = request.strip()
      LOG(LogLevel.INFO, 'executer has read input ' + request)
      status, result = self._handle_request(request)
      response = executer_utils.serialize_response(status, result)
      output.write(response + '\n')
