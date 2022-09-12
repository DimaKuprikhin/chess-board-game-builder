import random
import string


def generate_unique_string(n: int) -> str:
  return ''.join(
      random.choice(string.ascii_letters + string.digits) for _ in range(n)
  )
