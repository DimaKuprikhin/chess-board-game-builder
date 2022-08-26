import executer.script as script
import sys
from common.logger import LogLevel, LOG


class Executer:
  def __init__(self):
    return

  def run(self, input_iter):
    LOG(LogLevel.INFO, 'executer has been started')
    for command in input_iter:
      command = command.strip()
      LOG(LogLevel.INFO, 'executer has read input ' + command)
      if command == 'getArray':
        print(script.getArray(3))
      elif command == 'getMap':
        print(script.getMap(4, 'value'))
      elif command == 'getSquare':
        print(script.getSquare(7))
      else:
        break
      # There is no need to flush, but we do it just in case.
      sys.stdout.flush()
