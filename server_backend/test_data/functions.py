def get_array(length=3):
  result = []
  for i in range(length):
    result.append(i)
  return result


def get_map(key='key', value='value'):
  return { key: value }


def get_square(number=7):
  return number * number
