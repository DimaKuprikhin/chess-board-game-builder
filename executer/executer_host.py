import subprocess as sp
import sys
from typing import Any, Tuple
from executer import executer_utils


class ExecuterHost:
  '''
  Used to handle executer processes with Executer class instance.
  Provides API for creating executer process and inter-process
  communication with it to execute user scripts.
  '''
  def __init__(self, init_by_test=False):
    '''
    Executer created for testing by pytest needs specific resource limits.
    '''
    self.executer = None
    self.init_by_test = init_by_test

  def create_executer(self) -> bool:
    '''
    Creates a new process with Executer class instance running an endless
    loop for receiving requests and sending responces through IPC using json
    format.
    '''
    if self.executer:
      return False

    script = 'import sys;'
    script += 'from executer.executer import Executer;'
    if self.init_by_test:
      script += 'Executer(True).run(sys.stdin, sys.stdout)'
    else:
      script += 'Executer().run(sys.stdin, sys.stdout)'
    self.executer = sp.Popen([sys.executable, '-c', script],
                             stdin=sp.PIPE,
                             stdout=sp.PIPE,
                             universal_newlines=True)
    return True

  def call_script_function(
      self, module_name: str, function: str, args: list, timeout: float
  ) -> Tuple[bool, Any]:
    '''
    Sends request to executer to call a certain function from a certain module
    with the given arguments. Returns status of the call and result.
    '''
    if self.executer is None:
      return False, 'Executer hasn\'t been created'

    request_data = executer_utils.serialize_call_function_request(
        module_name, function, args, timeout
    )
    request = executer_utils.serialize_request('call_function', request_data)
    response = None
    # Executer process may no longer exist, so we need to handle possible
    # exceptions.
    try:
      self.executer.stdin.write(request + '\n')
      self.executer.stdin.flush()
      response = self.executer.stdout.readline().strip()
    except:
      return False, 'Error while communicating with executer'
    if not response:
      return False, 'No response from executer'
    return executer_utils.deserialize_response(response)

  def has_executer(self) -> bool:
    '''
    Returns true if `create_executer()` method was called earlier and finished
    successfully. True result doesn't mean executer is still running, use
    `is_alive()` for it.
    '''
    return self.executer is not None

  def is_alive(self) -> bool:
    '''
    Returns true if executer is still running and can be requested.
    '''
    if self.executer is None:
      return False
    return self.executer.poll() is None
