import enum
import sys


class LogLevel(enum.Enum):
  INFO = 1
  WARNING = 2
  ERROR = 3


def LOG(log_level, message):
  actual_message = ''
  if log_level == LogLevel.INFO:
    actual_message += 'INFO: '
  elif log_level == LogLevel.WARNING:
    actual_message += 'WARNING: '
  elif log_level == LogLevel.ERROR:
    actual_message += 'ERROR: '
  actual_message += message
  print(actual_message, file=sys.stderr)
