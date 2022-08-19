import subprocess as sp
import sys

def run_executer():
    return sp.Popen(
        [sys.executable, '-c', 'import executer; executer.run()'],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        universal_newlines=True)

def communicate(process, input):
    process.stdin.write(input + '\n')
    process.stdin.flush()
    print('LOG: wrote input')
    line = process.stdout.readline()
    if not line:
        return ''
    print('LOG: read output')
    return line

p = run_executer()
while p.poll() is None:
    print(communicate(p, input()), end='')
