import chess_rules


def move(from_x, from_y, to_x, to_y):
  return {'from_x': from_x, 'from_y': from_y, 'to_x': to_x, 'to_y': to_y}


def piece(name, color, x, y):
  return {'name': name, 'color': color, 'x': x, 'y': y}


def cmp_lists(lhs, rhs):
  if len(lhs) != len(rhs):
      return False
  for e in lhs:
    if len([el for el in rhs if e == el]) != 1:
      return False
  return True


class TestChessRules:
  def test_pawn_moves(self):
    pieces = [ piece('pawn', 'black', 2, 6) ]
    expected_moves = [
        move(2, 6, 2, 5),
        move(2, 6, 2, 4)
    ]
    assert chess_rules.get_possible_moves(pieces, 'black', {}) == expected_moves

    pieces.extend([
        piece('bishop', 'white', 1, 5),
        piece('dummy', 'black', 3, 5)
    ])
    expected_moves.append(move(2, 6, 1, 5))
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'black', {}), expected_moves)

  def test_bishop_moves(self):
    pieces = [ piece('bishop', 'white', 3, 2) ]
    expected_moves = [
        move(3, 2, 2, 1),
        move(3, 2, 1, 0),
        move(3, 2, 4, 3),
        move(3, 2, 5, 4),
        move(3, 2, 6, 5),
        move(3, 2, 7, 6),
        move(3, 2, 2, 3),
        move(3, 2, 1, 4),
        move(3, 2, 0, 5),
        move(3, 2, 4, 1),
        move(3, 2, 5, 0),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'white', {}), expected_moves)

    pieces.extend([
        piece('queen', 'black', 5, 4),
        piece('dummy', 'white', 5, 0)
    ])
    expected_moves = [
        move(3, 2, 2, 1),
        move(3, 2, 1, 0),
        move(3, 2, 4, 3),
        move(3, 2, 5, 4),
        move(3, 2, 2, 3),
        move(3, 2, 1, 4),
        move(3, 2, 0, 5),
        move(3, 2, 4, 1),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'white', {}), expected_moves)

  def test_rook_moves(self):
    pieces = [ piece('rook', 'black', 4, 5) ]
    expected_moves = [
        move(4, 5, 3, 5),
        move(4, 5, 2, 5),
        move(4, 5, 1, 5),
        move(4, 5, 0, 5),
        move(4, 5, 5, 5),
        move(4, 5, 6, 5),
        move(4, 5, 7, 5),
        move(4, 5, 4, 4),
        move(4, 5, 4, 3),
        move(4, 5, 4, 2),
        move(4, 5, 4, 1),
        move(4, 5, 4, 0),
        move(4, 5, 4, 6),
        move(4, 5, 4, 7),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'black', {}), expected_moves)

    pieces.extend([
        piece('dummy', 'black', 4, 3),
        piece('pawn', 'white', 4, 6)
    ])
    expected_moves = [
        move(4, 5, 3, 5),
        move(4, 5, 2, 5),
        move(4, 5, 1, 5),
        move(4, 5, 0, 5),
        move(4, 5, 5, 5),
        move(4, 5, 6, 5),
        move(4, 5, 7, 5),
        move(4, 5, 4, 4),
        move(4, 5, 4, 6),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'black', {}), expected_moves)

  def test_queen_moves(self):
    pieces = [{'name': 'queen', 'color': 'white', 'x': 2, 'y': 2}]
    expected_moves = [
        move(2, 2, 1, 1),
        move(2, 2, 0, 0),
        move(2, 2, 1, 2),
        move(2, 2, 0, 2),
        move(2, 2, 1, 3),
        move(2, 2, 0, 4),
        move(2, 2, 2, 1),
        move(2, 2, 2, 0),
        move(2, 2, 2, 3),
        move(2, 2, 2, 4),
        move(2, 2, 2, 5),
        move(2, 2, 2, 6),
        move(2, 2, 2, 7),
        move(2, 2, 3, 1),
        move(2, 2, 4, 0),
        move(2, 2, 3, 2),
        move(2, 2, 4, 2),
        move(2, 2, 5, 2),
        move(2, 2, 6, 2),
        move(2, 2, 7, 2),
        move(2, 2, 3, 3),
        move(2, 2, 4, 4),
        move(2, 2, 5, 5),
        move(2, 2, 6, 6),
        move(2, 2, 7, 7),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'white', {}), expected_moves)

    pieces.extend([
        piece('dummy', 'white', 2, 5),
        piece('dummy', 'black', 0, 0),
        piece('dummy', 'white', 2, 1),
        piece('dummy', 'black', 5, 5),
        piece('dummy', 'white', 4, 2),
    ])
    expected_moves = [
        move(2, 2, 1, 1),
        move(2, 2, 0, 0),
        move(2, 2, 1, 2),
        move(2, 2, 0, 2),
        move(2, 2, 1, 3),
        move(2, 2, 0, 4),
        move(2, 2, 2, 3),
        move(2, 2, 2, 4),
        move(2, 2, 3, 1),
        move(2, 2, 4, 0),
        move(2, 2, 3, 2),
        move(2, 2, 3, 3),
        move(2, 2, 4, 4),
        move(2, 2, 5, 5),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'white', {}), expected_moves)

  def test_knight_moves(self):
    pieces = [piece('knight', 'black', 6, 4)]
    expected_moves = [
        move(6, 4, 4, 3),
        move(6, 4, 4, 5),
        move(6, 4, 5, 2),
        move(6, 4, 5, 6),
        move(6, 4, 7, 2),
        move(6, 4, 7, 6),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'black', {}), expected_moves)

    pieces.extend([
        piece('dummy', 'black', 4, 5),
        piece('dummy', 'white', 4, 3)
    ])
    expected_moves = [
        move(6, 4, 4, 3),
        move(6, 4, 5, 2),
        move(6, 4, 5, 6),
        move(6, 4, 7, 2),
        move(6, 4, 7, 6),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'black', {}), expected_moves)

  def test_king_moves(self):
    # free to move anywhere
    pieces = [piece('king', 'white', 3, 3)]
    expected_moves = [
        move(3, 3, 2, 2),
        move(3, 3, 2, 3),
        move(3, 3, 2, 4),
        move(3, 3, 3, 2),
        move(3, 3, 3, 4),
        move(3, 3, 4, 2),
        move(3, 3, 4, 3),
        move(3, 3, 4, 4),
    ]
    additional_data = {'white_king_is_attacked': False, 'black_king_is_attacked': False}
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'white', additional_data), expected_moves)

    # can't step on pieces with the same color but can do it with other color
    pieces.extend([
        piece('dummy', 'white', 2, 3),
        piece('dummy', 'black', 3, 4),
        piece('dummy', 'white', 4, 4),
    ])
    expected_moves = [
        move(3, 3, 2, 2),
        move(3, 3, 2, 4),
        move(3, 3, 3, 2),
        move(3, 3, 3, 4),
        move(3, 3, 4, 2),
        move(3, 3, 4, 3)
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'white', additional_data), expected_moves)

    # castling
    pieces = [
        piece('king', 'black', 4, 7),
        piece('rook', 'black', 0, 7),
        piece('rook', 'black', 7, 7),
        piece('dummy', 'black', 0, 6),
        piece('dummy', 'black', 3, 6),
        piece('dummy', 'black', 4, 6),
        piece('dummy', 'black', 5, 6),
        piece('dummy', 'black', 7, 6)
    ]
    additional_data = {
        'black_king_moved': False,
        'black_a_rook_moved': False,
        'black_h_rook_moved': False,
        'white_king_is_attacked': False,
        'black_king_is_attacked': False
    }
    expected_moves = [
        move(4, 7, 3, 7),
        move(4, 7, 5, 7),
        move(4, 7, 2, 7),
        move(4, 7, 6, 7),
        move(0, 7, 1, 7),
        move(0, 7, 2, 7),
        move(0, 7, 3, 7),
        move(7, 7, 6, 7),
        move(7, 7, 5, 7),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'black', additional_data), expected_moves)

    # can't castle with a rook due to white rook
    pieces = [
        piece('king', 'black', 4, 7),
        piece('rook', 'black', 0, 7),
        piece('rook', 'black', 7, 7),
        piece('dummy', 'black', 0, 6),
        piece('dummy', 'black', 3, 6),
        piece('dummy', 'black', 4, 6),
        piece('dummy', 'black', 5, 6),
        piece('dummy', 'black', 7, 6),
        piece('rook', 'white', 2, 1)
    ]
    additional_data = {
        'black_king_moved': False,
        'black_a_rook_moved': False,
        'black_h_rook_moved': False,
        'white_king_is_attacked': False,
        'black_king_is_attacked': False
    }
    expected_moves = [
        move(4, 7, 3, 7),
        move(4, 7, 5, 7),
        move(4, 7, 6, 7),
        move(0, 7, 1, 7),
        move(0, 7, 2, 7),
        move(0, 7, 3, 7),
        move(7, 7, 6, 7),
        move(7, 7, 5, 7),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'black', additional_data), expected_moves)

    # can't castle with a rook due to white rook
    pieces = [
        piece('king', 'black', 4, 7),
        piece('rook', 'black', 0, 7),
        piece('rook', 'black', 7, 7),
        piece('dummy', 'black', 0, 6),
        piece('dummy', 'black', 4, 6),
        piece('dummy', 'black', 5, 6),
        piece('dummy', 'black', 7, 6),
        piece('rook', 'white', 3, 1)
    ]
    additional_data = {
        'black_king_moved': False,
        'black_a_rook_moved': False,
        'black_h_rook_moved': False,
        'white_king_is_attacked': False,
        'black_king_is_attacked': False
    }
    expected_moves = [
        move(4, 7, 5, 7),
        move(4, 7, 6, 7),
        move(0, 7, 1, 7),
        move(0, 7, 2, 7),
        move(0, 7, 3, 7),
        move(7, 7, 6, 7),
        move(7, 7, 5, 7),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'black', additional_data), expected_moves)

    # can't castle with h rook because this rook has moved
    pieces = [
        piece('king', 'white', 4, 0),
        piece('rook', 'white', 0, 0),
        piece('rook', 'white', 7, 0),
        piece('dummy', 'white', 0, 1),
        piece('dummy', 'white', 3, 1),
        piece('dummy', 'white', 4, 1),
        piece('dummy', 'white', 5, 1),
        piece('dummy', 'white', 7, 1)
    ]
    additional_data = {
        'white_king_moved': False,
        'white_a_rook_moved': False,
        'white_h_rook_moved': True,
        'white_king_is_attacked': False,
        'black_king_is_attacked': False
    }
    expected_moves = [
        move(4, 0, 3, 0),
        move(4, 0, 5, 0),
        move(4, 0, 2, 0),
        move(0, 0, 1, 0),
        move(0, 0, 2, 0),
        move(0, 0, 3, 0),
        move(7, 0, 6, 0),
        move(7, 0, 5, 0),
    ]
    assert cmp_lists(chess_rules.get_possible_moves(pieces, 'white', additional_data), expected_moves)

    # can't castle because the white king is under attack
    pieces = [
        piece('king', 'white', 4, 0),
        piece('rook', 'white', 0, 0),
        piece('rook', 'black', 3, 7),
        piece('dummy', 'white', 0, 1),
        piece('dummy', 'white', 3, 1),
        piece('dummy', 'white', 5, 1)
    ]
    additional_data = {
        'white_king_moved': False,
        'white_a_rook_moved': False,
        'white_h_rook_moved': True,
        'white_king_is_attacked': False,
        'black_king_is_attacked': False
    }
    expected_moves = [
        move(4, 0, 3, 0),
        move(4, 0, 5, 0)
    ]
    assert cmp_lists(
        chess_rules.make_move(pieces, move(3, 7, 4, 7), 'white', additional_data)['possible_moves'],
        expected_moves
    )

  def test_make_move(self):
    pieces = [
        piece('pawn', 'white', 0, 1)
    ]
    move_ = move(0, 1, 0, 2)
    game_state = chess_rules.make_move(pieces, move_, 'black', {})
    expected_pieces = [ piece('pawn', 'white', 0, 2) ]
    assert cmp_lists(game_state['pieces'], expected_pieces)
    assert cmp_lists(game_state['possible_moves'], [])

    game_state = chess_rules.get_starting_state()
    game_state = chess_rules.make_move(game_state['pieces'], move_, 'black', game_state['additional_data'])
