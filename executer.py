import script
import sys
from logger import LogLevel, LOG


class StdinIter(object):
  def __init__(self):
    return

  def __iter__(self):
    return self

  def __next__(self):
    for line in sys.stdin:
      yield line
    raise StopIteration


class Executer:
  def __init__(self):
    return

  def run(self, input_iter=StdinIter()):
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
