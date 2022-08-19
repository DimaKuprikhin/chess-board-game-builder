import subprocess as sp
import sys
from logger import LogLevel, LOG

executers = {}

def create_executer(executer_id):
    if executer_id in executers:
        LOG(LogLevel.ERROR, 'there is already an executer with id ' + executer_id)
    executers[executer_id] = sp.Popen(
        [sys.executable, '-c', 'import executer; executer.run()'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        universal_newlines=True)

def communicate(executer_id, input):
    if executer_id not in executers:
        LOG(LogLevel.ERROR, 'there is no executer with id ' + executer_id)
    executer = executers[executer_id]
    executer.stdin.write(input + '\n')
    executer.stdin.flush()
    line = executer.stdout.readline()
    if not line:
        LOG(LogLevel.INFO, 'executer ' + str(executer_id) + ' has finished work')
        return ''
    return line

create_executer(1)
create_executer(2)
while True:
    working_executers = 0
    if executers[1].poll() is None:
        working_executers += 1
        LOG(LogLevel.INFO, 'executer 1: ' + communicate(1, input()))
    if executers[2].poll() is None:
        working_executers += 1
        LOG(LogLevel.INFO, 'executer 2: ' + communicate(2, input()))
    if working_executers == 0:
        break
