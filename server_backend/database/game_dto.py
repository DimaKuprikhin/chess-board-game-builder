from typing_extensions import Self


class GameDTO:
  def __init__(
      self,
      id: int = None,
      first_player_id: int = None,
      second_player_id: int = None,
      first_player_plays_as: str = None,
      move_number: int = None,
      turn: str = None,
      script_id: int = None,
      link: str = None,
      game_state: str = None,
      additional_data: str = None
  ):
    self.id = id
    self.first_player_id = first_player_id
    self.second_player_id = second_player_id
    self.first_player_plays_as = first_player_plays_as
    self.move_number = move_number
    self.turn = turn
    self.script_id = script_id
    self.link = link
    self.game_state = game_state
    self.additional_data = additional_data

  def __eq__(self, other: Self) -> bool:
    return (
        isinstance(other, GameDTO) and self.id == other.id
        and self.first_player_id == other.first_player_id
        and self.second_player_id == other.second_player_id
        and self.first_player_plays_as == other.first_player_plays_as
        and self.move_number == other.move_number and self.turn == other.turn
        and self.script_id == other.script_id and self.link == other.link
        and self.game_state == other.game_state
        and self.additional_data == other.additional_data
    )

  def get_id(self) -> int:
    return self.id

  def get_first_player_id(self) -> int:
    return self.first_player_id

  def get_second_player_id(self) -> int:
    return self.second_player_id

  def get_first_player_plays_as(self) -> str:
    return self.first_player_plays_as

  def get_move_number(self) -> int:
    return self.move_number

  def get_turn(self) -> str:
    return self.turn

  def get_script_id(self) -> int:
    return self.script_id

  def get_link(self) -> str:
    return self.link

  def get_game_state(self) -> str:
    return self.game_state

  def get_additional_data(self) -> str:
    return self.additional_data

  def set_id(self, id: int) -> Self:
    self.id = id
    return self

  def set_first_player_id(self, id: int) -> Self:
    self.first_player_id = id
    return self

  def set_second_player_id(self, id: int) -> Self:
    self.second_player_id = id
    return self

  def set_first_player_plays_as(self, color: str) -> Self:
    self.first_player_plays_as = color
    return self

  def set_move_number(self, move_number: int) -> Self:
    self.move_number = move_number
    return self

  def set_turn(self, turn: str) -> Self:
    self.turn = turn
    return self

  def set_script_id(self, id: int) -> Self:
    self.script_id = id
    return self

  def set_link(self, link: str) -> Self:
    self.link = link
    return self

  def set_game_state(self, game_state: str) -> Self:
    self.game_state = game_state
    return self

  def set_additional_data(self, data: str) -> Self:
    self.additional_data = data
    return self

  def to_map(self) -> map:
    return {
        'id': self.id,
        'first_player_id': self.first_player_id,
        'second_player_id': self.second_player_id,
        'first_player_plays_as': self.first_player_plays_as,
        'move_number': self.move_number,
        'turn': self.turn,
        'script_id': self.script_id,
        'link': self.link,
        'game_state': self.game_state,
        'additional_data': self.additional_data
    }
