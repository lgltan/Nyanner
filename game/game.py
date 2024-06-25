# game functions
import numpy as np
from Player import Player
from pieces.King import King
from pieces.Pawn import Pawn
from pieces.Bishop import Bishop
from pieces.Knight import Knight
from pieces.Rook import Rook
from pieces.Queen import Queen

BOARD_COLS = 5
BOARD_ROWS = 8

def battle(p1_board, p2_board):
    # initializing boards from strings
    p1_board = np.reshape(p1_board.split(","), (-1, BOARD_COLS))
    p2_board = np.reshape(p2_board.lower().split(","), (-1, BOARD_COLS))
    # p2 needs to be mirrored and flipped upside down
    p2_board = np.flip(p2_board, (1, 0))
    # merging 2 player boards into game board
    nd_board = np.concatenate((p2_board, p1_board), 0)
    board = nd_board.flatten()
    
    print(nd_board)
    
    p1_win = False
    p2_win = False
    player_turn = 0
    # start main loop
    while p1_win == False and p2_win == False:
        if player_turn == 0:
            p1_win = player_move(board, player_turn)
            player_turn = 1
        elif player_turn == 1:
            p2_win = player_move(board, player_turn)
            player_turn = 0
            
def player_move(board, p_turn):
    if p_turn == 0:
        # move upper case pieces
        pass
    elif p_turn == 1:
        # move lower case pieces
        pass
    
    
    
    

        
p1 = Player()
p2 = Player()

battle(p1.board, p2.board)