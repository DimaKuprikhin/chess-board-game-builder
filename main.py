from executer_manager import ExecuterManager
from logger import LogLevel, LOG

manager = ExecuterManager()
manager.create_executer(1)
manager.create_executer(2)
while manager.is_any_alive():
    if manager.is_alive(1):
        LOG(LogLevel.INFO, 'executer 1: ' + manager.communicate(1, input()))
    if manager.is_alive(2):
        LOG(LogLevel.INFO, 'executer 2: ' + manager.communicate(2, input()))
