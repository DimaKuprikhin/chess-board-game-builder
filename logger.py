import enum
import sys

_is_logging_enabled = True


def ENABLE_LOGGING():
  global _is_logging_enabled
  _is_logging_enabled = True


def DISABLE_LOGGING():
  global _is_logging_enabled
  _is_logging_enabled = False


class LogLevel(enum.Enum):
  INFO = 1
  WARNING = 2
  ERROR = 3


def LOG(log_level, message):
  if not _is_logging_enabled:
    return
  actual_message = ''
  if log_level == LogLevel.INFO:
    actual_message += 'INFO: '
  elif log_level == LogLevel.WARNING:
    actual_message += 'WARNING: '
  elif log_level == LogLevel.ERROR:
    actual_message += 'ERROR: '
  actual_message += message
  print(actual_message, file=sys.stderr)
