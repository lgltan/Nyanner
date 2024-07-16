# game functions
import numpy as np
from sunfish import initial, Searcher, Position, MATE_LOWER, MATE_UPPER

BOARD_COLS = 8
BOARD_ROWS = 8

def battle(current_board):
    # convert board to sunfish layout
    nd_board = np.reshape(list(current_board), (-1, BOARD_COLS))
    nd_board = np.insert(nd_board, BOARD_ROWS, " ", axis=0)
    nd_board = np.insert(nd_board, BOARD_ROWS, " ", axis=0)
    nd_board = np.insert(nd_board, 0, " ", axis=0)
    nd_board = np.insert(nd_board, 0, " ", axis=0)
    nd_board = np.insert(nd_board, BOARD_COLS, "\n", axis=1)
    nd_board = np.insert(nd_board, 0, " ", axis=1)

    board = ''.join(nd_board.flatten().tolist())
    
    new_board, game_status = play_move(initial_positions=board)
    return new_board, game_status

def play_move(initial_positions=None, search_depth=5):
    if initial_positions is None:
        initial_positions = initial

    # Initialize the game with the given positions
    hist = [Position(initial_positions, 0, (True, True), (True, True), 0, 0)]

    searcher = Searcher()

    # Simulate the game up to a depth of search_depth
    for depth, gamma, score, move in searcher.search(hist):
        if depth == search_depth:
            break
        
    new_board = Position(initial_positions, 0, (True, True), (True, True), 0, 0).move(move)

    # Check for end of game conditions (checkmate, stalemate, etc.)
    # This is a simplified check; you might want to implement a more thorough check
    if score == MATE_UPPER:
        return new_board.board, "k"
    elif score == MATE_LOWER:
        return new_board.board, "K"
    else:
        return new_board.board, "c"

# new_board = (
#     "rnbqkbnr"
#     "pppppppp"
#     "........"
#     "........"
#     "........"
#     "........"
#     "PPPPPPPP"
#     "RNBQKBNR"
#     )

# current_board, status = battle(new_board)
# print(current_board)