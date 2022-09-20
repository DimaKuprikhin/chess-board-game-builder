from copy import deepcopy


def do_get_possible_moves(pieces, turn, additional_data):
  possible_moves = []

  def get_pieces(name, color):
    return [p for p in pieces if p['color'] == color and p['name'] == name]

  def piece_at(x, y):
    result = [p for p in pieces if p['x'] == x and p['y'] == y]
    return result[0] if len(result) == 1 else None

  def in_bounds(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

  def is_white(x, y):
    return len([p for p in pieces if p['color'] == 'white' and p['x'] == x and p['y'] == y]) == 1

  def is_black(x, y):
    return len([p for p in pieces if p['color'] == 'black' and p['x'] == x and p['y'] == y]) == 1

  def is_opposite(x, y, color):
    return is_white(x, y) if color == 'black' else is_black(x, y)

  def is_free(x, y):
    return len([p for p in pieces if p['x'] == x and p['y'] == y]) == 0

  def add_move(from_x, from_y, to_x, to_y):
    possible_moves.append({'from_x': from_x, 'from_y': from_y, 'to_x': to_x, 'to_y': to_y})

  # TODO: en passant
  def handle_white_pawn(x, y):
    if is_free(x, y + 1):
      add_move(x, y, x, y + 1)
      if y == 1 and is_free(x, y + 2):
        add_move(x, y, x, y + 2)
    if in_bounds(x - 1, y + 1) and is_black(x - 1, y + 1):
      add_move(x, y, x - 1, y + 1)
    if in_bounds(x + 1, y + 1) and is_black(x + 1, y + 1):
      add_move(x, y, x + 1, y + 1)

  # TODO: en passant
  def handle_black_pawn(x, y):
    if is_free(x, y - 1):
      add_move(x, y, x, y - 1)
      if y == 6 and is_free(x, y - 2):
        add_move(x, y, x, y - 2)
    if in_bounds(x - 1, y - 1) and is_white(x - 1, y - 1):
      add_move(x, y, x - 1, y - 1)
    if in_bounds(x + 1, y - 1) and is_white(x + 1, y - 1):
      add_move(x, y, x + 1, y - 1)

  def handle_knight(x, y, color):
    for dy in range(-2, 3):
      if dy == 0: continue
      for dx in range(-3 + abs(dy), 3, 6 - 2 * abs(dy)):
        to_x = x + dx
        to_y = y + dy
        if in_bounds(to_x, to_y) and (is_free(to_x, to_y) or is_opposite(to_x, to_y, color)):
          add_move(x, y, to_x, to_y)

  def handle_bishop(x, y, color):
    for dy in range(-1, 2, 2):
      for dx in range(-1, 2, 2):
        for n in range(1, 8):
          to_x = x + n * dx
          to_y = y + n * dy
          if not in_bounds(to_x, to_y) or not is_free(to_x, to_y) and not is_opposite(to_x, to_y, color):
            break
          add_move(x, y, to_x, to_y)
          if is_opposite(to_x, to_y, color):
            break

  def handle_rook(x, y, color):
    for dy in range(-1, 2):
      for dx in range(-1 + abs(dy), 2, 2):
        for n in range(1, 8):
          to_x = x + n * dx
          to_y = y + n * dy
          if not in_bounds(to_x, to_y) or not is_free(to_x, to_y) and not is_opposite(to_x, to_y, color):
            break
          add_move(x, y, to_x, to_y)
          if is_opposite(to_x, to_y, color):
            break

  def handle_queen(x, y, color):
    for dy in range(-1, 2):
      for dx in range(-1, 2):
        if dy == 0 and dx == 0:
          continue
        for n in range(1, 8):
          to_x = x + n * dx
          to_y = y + n * dy
          if not in_bounds(to_x, to_y) or not is_free(to_x, to_y) and not is_opposite(to_x, to_y, color):
            break
          add_move(x, y, to_x, to_y)
          if is_opposite(to_x, to_y, color):
            break

  def handle_white_king(x, y):
    for dy in range(-1, 2):
      for dx in range(-1, 2):
        if dy == 0 and dx == 0:
          continue
        to_x = x + dx
        to_y = y + dy
        if in_bounds(to_x, to_y) and (is_opposite(to_x, to_y, 'white') or is_free(to_x, to_y)):
          add_move(x, y, to_x, to_y)
    if additional_data['white_king_is_attacked']:
      return
    rook = piece_at(0, 0)
    if (x == 4 and y == 0 and rook is not None and rook['name'] == 'rook' and rook['color'] == turn
        and not additional_data['white_king_moved'] and not additional_data['white_a_rook_moved']
        and is_free(1, 0) and is_free(2, 0) and is_free(3, 0)):
      add_move(x, y, x - 2, y)
    rook = piece_at(7, 0)
    if (x == 4 and y == 0 and rook is not None and rook['name'] == 'rook' and rook['color'] == turn
        and not additional_data['white_king_moved'] and not additional_data['white_h_rook_moved']
        and is_free(5, 0) and is_free(6, 0)):
      add_move(x, y, x + 2, y)

  def handle_black_king(x, y):
    for dy in range(-1, 2):
      for dx in range(-1, 2):
        if dy == 0 and dx == 0:
          continue
        to_x = x + dx
        to_y = y + dy
        if in_bounds(to_x, to_y) and (is_opposite(to_x, to_y, 'black') or is_free(to_x, to_y)):
          add_move(x, y, to_x, to_y)
    if additional_data['black_king_is_attacked']:
      return
    rook = piece_at(0, 7)
    if (x == 4 and y == 7 and rook is not None and rook['name'] == 'rook' and rook['color'] == turn
        and not additional_data['black_king_moved'] and not additional_data['black_a_rook_moved']
        and is_free(1, 7) and is_free(2, 7) and is_free(3, 7)):
      add_move(x, y, x - 2, y)
    rook = piece_at(7, 7)
    if (x == 4 and y == 7 and rook is not None and rook['name'] == 'rook' and rook['color'] == turn
        and not additional_data['black_king_moved'] and not additional_data['black_h_rook_moved']
        and is_free(5, 7) and is_free(6, 7)):
      add_move(x, y, x + 2, y)

  if turn == 'white':
    for pawn in get_pieces('pawn', turn):
      handle_white_pawn(pawn['x'], pawn['y'])
    white_king = get_pieces('king', turn)
    if len(white_king) > 0:
      handle_white_king(white_king[0]['x'], white_king[0]['y'])
  else:
    for pawn in get_pieces('pawn', turn):
      handle_black_pawn(pawn['x'], pawn['y'])
    black_king = get_pieces('king', turn)
    if len(black_king) > 0:
      handle_black_king(black_king[0]['x'], black_king[0]['y'])

  for knight in get_pieces('knight', turn):
    handle_knight(knight['x'], knight['y'], turn)
  for bishop in get_pieces('bishop', turn):
    handle_bishop(bishop['x'], bishop['y'], turn)
  for rook in get_pieces('rook', turn):
    handle_rook(rook['x'], rook['y'], turn)
  for queen in get_pieces('queen', turn):
    handle_queen(queen['x'], queen['y'], turn)

  return possible_moves

def filter_possible_moves(pieces, turn, additional_data, moves):
  king = [p for p in pieces if p['color'] == turn and p['name'] == 'king']
  if len(king) == 0:
    return deepcopy(moves)
  king = deepcopy(king[0])
  king_backup = deepcopy(king)
  moves_ = []
  for move in moves:
    is_castling = king['x'] == move['from_x'] and king['y'] == move['from_y'] and abs(move['from_x'] - move['to_x']) == 2
    if king['x'] == move['from_x'] and king['y'] == move['from_y']:
      king['x'] = move['to_x']
      king['y'] = move['to_y']
    valid = True
    next_state = do_make_move(pieces, move, additional_data)
    possible_moves = do_get_possible_moves(
        next_state['pieces'], ('black' if turn == 'white' else 'white'), next_state['additional_data']
    )
    for possible_move in possible_moves:
      if possible_move['to_x'] == king['x'] and possible_move['to_y'] == king['y']:
        valid = False
      # can't castle if any cell between `from_x` and `to_x` is attacked by opposite pieces
      if (is_castling and (
          (move['from_x'] == 4 and move['to_x'] == 2 and possible_move['to_x'] == 3 and possible_move['to_y'] == move['to_y']) or
          (move['from_x'] == 4 and move['to_x'] == 6 and possible_move['to_x'] == 5 and possible_move['to_y'] == move['to_y']))
      ):
        valid = False
      if not valid:
        break
    if valid:
      moves_.append(move)
    king = deepcopy(king_backup)
  return moves_

def get_possible_moves(pieces, turn, additional_data):
  moves = do_get_possible_moves(pieces, turn, additional_data)
  moves = filter_possible_moves(pieces, turn, additional_data, moves)
  # white_king = [p for p in pieces if p['color'] == 'white' and p['name'] == 'king']
  # black_king = [p for p in pieces if p['color'] == 'black' and p['name'] == 'king']
  # if white_king is not None and len(white_king) > 0:
  #   white_king = white_king[0]
  #   additional_data['white_king_is_attacked'] = False
  #   if [m for m in moves if m['to_x'] == white_king['x'] and m['to_y'] == white_king['y']] is not None:
  #     additional_data['white_king_is_attacked'] = True
  # if black_king is not None and len(black_king) > 0:
  #   black_king = black_king[0]
  #   additional_data['black_king_is_attacked'] = False
  #   if [m for m in moves if m['to_x'] == black_king['x'] and m['to_y'] == black_king['y']] is not None:
  #     additional_data['black_king_is_attacked'] = True
  return moves

def do_make_move(pieces, move, additional_data):
  def piece_at(x, y):
    result = [p for p in pieces if p['x'] == x and p['y'] == y]
    return result[0] if len(result) == 1 else None

  x = move['from_x']
  y = move['from_y']
  to_x = move['to_x']
  to_y = move['to_y']
  pieces_ = deepcopy(pieces)
  additional_data_ = deepcopy(additional_data)
  # castling
  if piece_at(x, y)['name'] == 'king' and abs(to_x - x) == 2:
    king = deepcopy(piece_at(x, y))
    rook = deepcopy(piece_at(x - 4, y) if to_x < x else piece_at(x + 3, y))
    pieces_.remove(king)
    pieces_.remove(rook)
    king['x'] = to_x
    rook['x'] = to_x + 1 if to_x < x else to_x - 1
    pieces_.append(king)
    pieces_.append(rook)
    if king['color'] == 'white':
      additional_data_['white_king_moved'] = True
      if to_x == 2:
        additional_data_['white_a_rook_moved'] = True
      else:
        additional_data_['white_h_rook_moved'] = True
    else:
      additional_data_['black_king_moved'] = True
      if to_x == 2:
        additional_data_['black_a_rook_moved'] = True
      else:
        additional_data_['black_h_rook_moved'] = True
  # promotion
  elif piece_at(x, y)['name'] == 'pawn' and to_y == (0 if piece_at(x, y)['color'] == 'black' else 7):
    pawn = deepcopy(piece_at(x, y))
    pieces_.remove(pawn)
    pieces_.append({ 'name': 'queen', 'color': pawn['color'], 'x': to_x, 'y': to_y })
  else:
    captured = deepcopy(piece_at(to_x, to_y))
    moved = deepcopy(piece_at(x, y))
    if captured is not None:
      pieces_.remove(captured)
    pieces_.remove(moved)
    moved['x'] = to_x
    moved['y'] = to_y
    pieces_.append(moved)
    if moved['name'] == 'king':
      if moved['color'] == 'white':
        additional_data_['white_king_moved'] = True
      else:
        additional_data_['black_king_moved'] = True
    if moved['name'] == 'rook':
      if x == 0 and y == 0:
        additional_data_['white_a_rook_moved'] = True
      elif x == 7 and y == 0:
        additional_data_['white_h_rook_moved'] = True
      elif x == 0 and y == 7:
        additional_data_['black_a_rook_moved'] = True
      elif x == 7 and y == 7:
        additional_data_['black_h_rook_moved'] = True
  return {
    'pieces': pieces_,
    'additional_data': additional_data_
  }

def get_starting_state():
  pieces =  [
        { 'name': 'pawn', 'color': 'white', 'x': 0, 'y': 1 },
        { 'name': 'pawn', 'color': 'white', 'x': 1, 'y': 1 },
        { 'name': 'pawn', 'color': 'white', 'x': 2, 'y': 1 },
        { 'name': 'pawn', 'color': 'white', 'x': 3, 'y': 1 },
        { 'name': 'pawn', 'color': 'white', 'x': 4, 'y': 1 },
        { 'name': 'pawn', 'color': 'white', 'x': 5, 'y': 1 },
        { 'name': 'pawn', 'color': 'white', 'x': 6, 'y': 1 },
        { 'name': 'pawn', 'color': 'white', 'x': 7, 'y': 1 },
        { 'name': 'rook', 'color': 'white', 'x': 0, 'y': 0 },
        { 'name': 'rook', 'color': 'white', 'x': 7, 'y': 0 },
        { 'name': 'knight', 'color': 'white', 'x': 1, 'y': 0 },
        { 'name': 'knight', 'color': 'white', 'x': 6, 'y': 0 },
        { 'name': 'bishop', 'color': 'white', 'x': 2, 'y': 0 },
        { 'name': 'bishop', 'color': 'white', 'x': 5, 'y': 0 },
        { 'name': 'king', 'color': 'white', 'x': 4, 'y': 0 },
        { 'name': 'queen', 'color': 'white', 'x': 3, 'y': 0 },
        { 'name': 'pawn', 'color': 'black', 'x': 0, 'y': 6 },
        { 'name': 'pawn', 'color': 'black', 'x': 1, 'y': 6 },
        { 'name': 'pawn', 'color': 'black', 'x': 2, 'y': 6 },
        { 'name': 'pawn', 'color': 'black', 'x': 3, 'y': 6 },
        { 'name': 'pawn', 'color': 'black', 'x': 4, 'y': 6 },
        { 'name': 'pawn', 'color': 'black', 'x': 5, 'y': 6 },
        { 'name': 'pawn', 'color': 'black', 'x': 6, 'y': 6 },
        { 'name': 'pawn', 'color': 'black', 'x': 7, 'y': 6 },
        { 'name': 'rook', 'color': 'black', 'x': 0, 'y': 7 },
        { 'name': 'rook', 'color': 'black', 'x': 7, 'y': 7 },
        { 'name': 'knight', 'color': 'black', 'x': 1, 'y': 7 },
        { 'name': 'knight', 'color': 'black', 'x': 6, 'y': 7 },
        { 'name': 'bishop', 'color': 'black', 'x': 2, 'y': 7 },
        { 'name': 'bishop', 'color': 'black', 'x': 5, 'y': 7 },
        { 'name': 'king', 'color': 'black', 'x': 4, 'y': 7 },
        { 'name': 'queen', 'color': 'black', 'x': 3, 'y': 7 }
    ]
  additional_data = {
        'white_king_moved': False,
        'black_king_moved': False,
        'white_a_rook_moved': False,
        'white_h_rook_moved': False,
        'black_a_rook_moved': False,
        'black_h_rook_moved': False,
        'white_king_is_attacked': False,
        'black_king_is_attacked': False
    }
  return {
    'pieces': pieces,
    'possible_moves': get_possible_moves(pieces, 'white', additional_data),
    'additional_data': additional_data,
    'status': 'running'
  }

def make_move(pieces, move, next_turn, additional_data):
  result = do_make_move(pieces, move, additional_data)
  pieces_ = result['pieces']
  additional_data_ = result['additional_data']

  additional_data_['white_king_is_attacked'] = False
  additional_data_['black_king_is_attacked'] = False
  king = [p for p in pieces_ if p['color'] == next_turn and p['name'] == 'king']
  if king is not None and len(king) > 0:
    king = king[0]
    next_possible_moves = get_possible_moves(
        pieces_, 'white' if next_turn == 'black' else 'black', additional_data_
    )
    king_attacking_moves = [m for m in next_possible_moves if m['to_x'] == king['x'] and m['to_y'] == king['y']]
    if king_attacking_moves is not None and len(king_attacking_moves) > 0:
      additional_data_[next_turn + '_king_is_attacked'] = True

  possible_moves = get_possible_moves(pieces_, next_turn, additional_data_)

  status = 'running'
  if len(possible_moves) == 0:
    status = ('white' if next_turn == 'black' else 'black') + ' won'
  return {
    'pieces': pieces_,
    'possible_moves': possible_moves,
    'additional_data': additional_data_,
    'status': status
  }
