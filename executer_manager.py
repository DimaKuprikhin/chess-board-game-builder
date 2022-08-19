import subprocess as sp
import sys
from logger import LogLevel, LOG

class ExecuterManager:
    def __init__(self):
        self.executers = {}
        self.running_count = 0
    
    def create_executer(self, executer_id):
        if executer_id in self.executers:
            LOG(LogLevel.ERROR, 'there is already an executer with id ' + executer_id)
            return
        self.executers[executer_id] = sp.Popen(
            [sys.executable, '-c', 'import executer; executer.run()'],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            universal_newlines=True)
        self.running_count += 1

    def communicate(self, executer_id, input):
        if executer_id not in self.executers:
            LOG(LogLevel.ERROR, 'there is no executer with id ' + executer_id)
            return ''
        executer = self.executers[executer_id]
        executer.stdin.write(input + '\n')
        executer.stdin.flush()
        line = executer.stdout.readline()
        if not line:
            LOG(LogLevel.INFO, 'executer ' + str(executer_id) + ' has finished work')
            self.running_count -= 1
            return ''
        return line
    
    def is_alive(self, executer_id):
        if executer_id not in self.executers:
            return False
        return self.executers[executer_id].poll() is None
    
    def is_any_alive(self):
        return self.running_count > 0
