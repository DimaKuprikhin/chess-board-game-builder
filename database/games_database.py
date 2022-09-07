class GamesDatabase:
  class Entry:
    def __init__(self, script_id: int, game_state):
      self.script_id = script_id
      self.game_state = game_state

    def get_game_state(self):
      return self.game_state

    def set_game_state(self, game_state):
      self.game_state = game_state

    def get_script_id(self):
      return self.script_id

  def __init__(self):
    self.games = {}

  def add_game(self, user_id: int, script_id: int, game_state) -> bool:
    '''
    Adds a new entry in the database. On success, returns True. If the database
    already contains an entry with the given user id, doesn't change its state
    and returns False.
    '''
    if user_id in self.games:
      return False
    self.games[user_id] = GamesDatabase.Entry(script_id, game_state)
    return True

  def get_script_id(self, user_id: int) -> int:
    '''
    Returns script id of the entry with the giver user id. If the database
    doesn't contain an entry with this user id, returns None.
    '''
    if user_id not in self.games:
      return None
    return self.games[user_id].get_script_id()

  def get_game_state(self, user_id: int):
    if user_id not in self.games:
      return None
    return self.games[user_id].get_game_state()

  def update_game_state(self, user_id: int, game_state) -> bool:
    if user_id not in self.games:
      return False
    self.games[user_id].set_game_state(game_state)
    return True

  def remove_game(self, user_id: int) -> bool:
    '''
    Removes an entry with the given user id from the database. If the database
    doesn't contain an entry with this user id, returns False and doesn't
    change its state.
    '''
    if user_id not in self.games:
      return False
    self.games.pop(user_id)
    return True
