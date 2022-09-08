import os
import pathlib


class ScriptsDatabase:
  class Entry:
    def __init__(self, module_name: str, script_path: str):
      self.module_name = module_name
      self.script_path = script_path

    def get_module_name(self) -> str:
      return self.module_name

    def get_script_path(self) -> str:
      return self.script_path

  def __init__(
      self, db_dir_path: pathlib.PosixPath, base_module_name: str = ''
  ):
    '''
    Creates a directory with path `db_dir_path` which will contain file for all
    the stored scripts. These scripts can be imported by other modules by
    module names got from `get_module_name` method. `base_module_name` will be
    a prefix for module names of stored scripts and must correspond
    `db_dir_path`.
    '''
    assert isinstance(db_dir_path, pathlib.PosixPath)
    assert isinstance(base_module_name, str)
    self.db_dir_path = db_dir_path
    if not os.path.exists(db_dir_path):
      os.mkdir(db_dir_path)
    self.base_module_name = base_module_name
    self.next_free_id = 1
    self.scripts = {}

  def add_script(self, script: str) -> int:
    '''
    Adds user script to scripts database, creates a unique module name and
    a file in `db_dir_path`. On success, returns script id, which can be used
    to access this database data.
    '''
    script_id = self.next_free_id
    self.next_free_id += 1
    module_name = self.base_module_name + '.' + str(script_id)
    script_path = self.db_dir_path.joinpath(str(script_id) + '.py')
    self.scripts[script_id] = ScriptsDatabase.Entry(module_name, script_path)
    with open(script_path, 'w') as f:
      f.write(script)
    return script_id

  def contains(self, script_id: int) -> bool:
    '''
    Returns True, if the database contains an entry with the given script id.
    '''
    return script_id in self.scripts

  def get_module_name(self, script_id: int) -> str:
    '''
    Returns a unique scripts module name, which can be imported in other
    modules. Returns None, if there is no script with the given script_id in
    database.
    '''
    if script_id not in self.scripts:
      return None
    return self.scripts[script_id].get_module_name()

  def remove_script(self, script_id: int) -> bool:
    '''
    Removes a script entry from the database and script file from `db_dir_path`
    directory. On success, returns True, otherwise False. May throw exceptions.
    '''
    if script_id not in self.scripts:
      return False
    path = self.scripts[script_id].get_script_path()
    self.scripts.pop(script_id)
    os.remove(path)
    return True
