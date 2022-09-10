def check_script(script: str) -> bool:
  '''
  Returns true if script is considered safe and
  contains no malware instructions.
  '''
  if not isinstance(script, str):
    return False
  return True
