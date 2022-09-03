def run_heavy_function():
  return fibonacci(100)


def fibonacci(n):
  if n < 2:
    return n
  return fibonacci(n - 1) + fibonacci(n - 2)

def heavy_power():
  '''
  Example from https://code.activestate.com/recipes/496746-restricted-safe-eval/.
  '''
  return 82173821737213782173821739921**881230980921832173821732132323798321
