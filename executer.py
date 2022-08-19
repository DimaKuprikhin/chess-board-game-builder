import script

import sys

def run():
    print('LOG: run', file=sys.stderr)
    while True:
        command = input()
        print('LOG: read input', file=sys.stderr)
        if command == 'getArray':
            print(script.getArray(3))
        elif command == 'getMap':
            print(script.getMap(4, 'value'))
        elif command == 'getSquare':
            print(script.getSquare(7))
        else:
            break
        # There is no need to flush, but we do it.
        sys.stdout.flush()
