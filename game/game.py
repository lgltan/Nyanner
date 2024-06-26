# game functions
import numpy as np
from sunfish import initial, Searcher, Position, MATE_LOWER, MATE_UPPER

from Player import Player

BOARD_COLS = 8
BOARD_ROWS = 8

def battle(p1_board, p2_board):
    # set up board for the game
    # initializing boards from strings
    p1_board = np.reshape(list(p1_board), (-1, BOARD_COLS))
    p2_board = np.reshape(list(p2_board.lower()), (-1, BOARD_COLS))
    # p2 needs to be mirrored and flipped upside down
    p2_board = np.flip(p2_board, (1, 0))
    # merging 2 player boards into game board
    nd_board = np.concatenate((p2_board, p1_board), 0)
    # convert board to sunfish layout
    nd_board = np.insert(nd_board, BOARD_ROWS, " ", axis=0)
    nd_board = np.insert(nd_board, BOARD_ROWS, " ", axis=0)
    nd_board = np.insert(nd_board, 0, " ", axis=0)
    nd_board = np.insert(nd_board, 0, " ", axis=0)
    nd_board = np.insert(nd_board, BOARD_COLS, "\n", axis=1)
    nd_board = np.insert(nd_board, 0, " ", axis=1)

    board = ''.join(nd_board.flatten().tolist())
    
    winner, move_count, board_list = play_self_game(initial_positions=board, max_moves=50)
    
    if winner == "K":
        print("P1 won")
        print(move_count)
        print(board_list[-1])
    elif winner == "k":
        print("P2 won")
        print(move_count)
        print(board_list[-1])
    else:
        print("Evaluate board")
        print(move_count)
        print(board_list[-1])

def play_self_game(initial_positions=None, max_moves=50, search_depth=3):
    if initial_positions is None:
        initial_positions = initial

    # Initialize the game with the given positions
    hist = [Position(initial_positions, 0, (True, True), (True, True), 0, 0)]

    searcher = Searcher()
    move_count = 0  # Initialize move counter

    while True:
        # Increment the move counter
        move_count += 1

        # Break the loop if the maximum number of moves is reached
        if move_count > max_moves:
            print("Game ended after reaching the maximum number of moves.")
            return 0, move_count, hist

        # Simulate the game up to a depth of search_depth
        for depth, gamma, score, move in searcher.search(hist):
            if depth == search_depth:
                break

        # Print the move made by the engine
        if move:
            hist.append(hist[-1].move(move))

        # Check for end of game conditions (checkmate, stalemate, etc.)
        # This is a simplified check; you might want to implement a more thorough check
        if score == MATE_UPPER:
            return "k", move_count, hist
        elif score == MATE_LOWER:
            return "K", move_count, hist