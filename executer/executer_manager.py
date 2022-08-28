import subprocess as sp
import sys
from typing import Any, Tuple
from common.logger import LogLevel, LOG
from executer import executer_utils


class ExecuterManager:
  '''
  Used to handle executer processes with Executer class instances in them.
  Provides API for creating executer processes and inter-process
  communication with them to load and execute user scripts.
  '''
  def __init__(self):
    self.executers = {}
    self.running_count = 0

  def create_executer(self, executer_id: str):
    '''
    Creates a new process with Executer class instance running an endless
    loop for receiving requests and sending responces through IPC using json
    format.
    '''
    if executer_id in self.executers:
      LOG(
          LogLevel.ERROR, 'there is already an executer with id ' + executer_id
      )
      return

    script = 'import sys; from executer.executer import Executer; Executer().run(sys.stdin, sys.stdout)'
    self.executers[executer_id] = sp.Popen([sys.executable, '-c', script],
                                           stdin=sp.PIPE,
                                           stdout=sp.PIPE,
                                           universal_newlines=True)
    self.running_count += 1

  def call_script_function(
      self, executer_id: str, module_name: str, function: str, args: list
  ) -> Tuple[bool, Any]:
    '''
    Sends request to executer to call a certain function from a certain module with the given
    arguments. Returns status of the call and result.
    '''
    if executer_id not in self.executers:
      LOG(LogLevel.ERROR, 'there is no executer with id ' + executer_id)
      return None

    executer = self.executers[executer_id]
    request_data = executer_utils.serialize_call_function_request(
        module_name, function, args
    )
    request = executer_utils.serialize_request('call_function', request_data)
    response = None
    # Executer process may no longer exist, so we need to handle possible
    # exceptions.
    try:
      executer.stdin.write(request + '\n')
      executer.stdin.flush()
      response = executer.stdout.readline().strip()
    except:
      pass
    if not response:
      self.running_count -= 1
      return None
    return executer_utils.deserialize_response(response)

  def is_alive(self, executer_id: str) -> bool:
    if executer_id not in self.executers:
      return False
    return self.executers[executer_id].poll() is None

  def is_any_alive(self) -> bool:
    return self.running_count > 0
