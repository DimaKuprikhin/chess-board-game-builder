import subprocess as sp
import sys
from common.logger import LogLevel, LOG
from executer.executer_utils import serialize_function_call, deserialize_function_result


class ExecuterManager:
  def __init__(self):
    self.executers = {}
    self.running_count = 0

  def create_executer(self, executer_id):
    if executer_id in self.executers:
      LOG(
          LogLevel.ERROR, 'there is already an executer with id ' + executer_id
      )
      return
    script = 'import sys; from executer.executer import Executer; Executer().run(sys.stdin)'
    self.executers[executer_id] = sp.Popen([sys.executable, '-c', script],
                                           stdin=sp.PIPE,
                                           stdout=sp.PIPE,
                                           universal_newlines=True)
    self.running_count += 1

  def communicate(self, executer_id, function, args):
    if executer_id not in self.executers:
      LOG(LogLevel.ERROR, 'there is no executer with id ' + executer_id)
      return ''

    executer = self.executers[executer_id]
    request = serialize_function_call(function, args)
    response = None
    try:
      executer.stdin.write(request + '\n')
      executer.stdin.flush()
      response = executer.stdout.readline().strip()
    except:
      pass
    if not response:
      LOG(LogLevel.INFO, 'executer ' + str(executer_id) + ' has finished work')
      self.running_count -= 1
      return ''
    return deserialize_function_result(response)

  def is_alive(self, executer_id):
    if executer_id not in self.executers:
      return False
    return self.executers[executer_id].poll() is None

  def is_any_alive(self):
    return self.running_count > 0
