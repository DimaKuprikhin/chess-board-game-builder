import executer.script as script
import sys
from common.logger import LogLevel, LOG
from executer.executer_utils import serialized_function_result, deserialize_function_call


class Executer:
  def __init__(self):
    return

  def run(self, input_iter):
    LOG(LogLevel.INFO, 'executer has been started')
    for command in input_iter:
      command = command.strip()
      LOG(LogLevel.INFO, 'executer has read input ' + command)
      function, args = deserialize_function_call(command)
      result = getattr(script, function)(*args)
      sys.stdout.write(serialized_function_result(result) + '\n')
      # There is no need to flush, but we do it just in case.
      sys.stdout.flush()
