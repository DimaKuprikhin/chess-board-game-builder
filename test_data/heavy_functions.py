def _fibonacci(n):
  if n < 2:
    return n
  return _fibonacci(n - 1) + _fibonacci(n - 2)


def heavy_function():
  return _fibonacci(100)


def heavy_power():
  '''
  Example from https://code.activestate.com/recipes/496746-restricted-safe-eval/.
  '''
  return 82173821737213782173821739921**881230980921832173821732132323798321
