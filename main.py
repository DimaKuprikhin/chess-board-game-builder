from executer.executer_manager import ExecuterManager
from common.logger import LogLevel, LOG
import sys


def _next_id(id, max_id):
  id += 1
  if id > max_id:
    return 1
  return id


def main():
  manager = ExecuterManager()
  manager.create_executer(1)
  manager.create_executer(2)
  total_executers = 2
  cur_executer = 1
  for line in sys.stdin:
    while not manager.is_alive(cur_executer):
      cur_executer = _next_id(cur_executer, total_executers)
    LOG(
        LogLevel.INFO, 'executer ' + str(cur_executer) + ': '
        + str(manager.communicate(cur_executer, line.strip(), []))
    )
    cur_executer = _next_id(cur_executer, total_executers)
    if not manager.is_any_alive():
      break


if __name__ == "__main__":
  main()
