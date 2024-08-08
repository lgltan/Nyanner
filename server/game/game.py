# game functions
import numpy as np
from server.game.sunfish import initial, Searcher, Position, MATE_LOWER, MATE_UPPER
import chess
import math

# For internal testing only
class Moves:
    def __init__(self, moves_id, lobby_id, board):
        self.moves_id = moves_id # probably move number
        self.lobby_id = lobby_id # foreign key
        self.board = board

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

cols:dict = {
    0 :'a',
    1 :'b',
    2 :'c',
    3 :'d',
    4 :'e',
    5 :'f',
    6 :'g',
    7 :'h'
}

# return uci based on both board states
def get_uci(old_board:str, new_board:str):
    
    promoted_piece:str = ''

    piece_position:dict = {}
    pos:str = ''
    uci:str = ''

    col:str = ''
    row:int = 0

    o:int = 0
    while o < 64:
        # check for differences between boards
        if old_board[o] != new_board[o]:
            # get column letter from cols dictionary
            col = cols[o%8]
            pos = pos + col
            
            # get row number
            inverted_o = (o - 64)*-1 # since count starts from top left, invert o to get actual row number
            row = math.ceil(inverted_o/8)
            pos = pos + str(row)

            # get piece moved
            piece = new_board[o]

            # check for promotions
            if (old_board[o] == 'p') & (row == 2):
                promoted_piece = promoted_piece + new_board[o+8]
            elif (old_board[o] == 'P') & (row == 7):
                promoted_piece = promoted_piece + new_board[o-8]

            piece_position.update({o : pos}) # save index and move for later searching
            pos = ''
        o+=1

    # identify first and second posiiton
    first_key = list(piece_position.keys())[0]
    second_key = list(piece_position.keys())[1]
    
    if old_board[first_key] != '.':
        uci = uci + piece_position[first_key] + piece_position[second_key]
    else:
        uci = uci + piece_position[second_key] + piece_position[first_key] 

    # append promotion notation
    if promoted_piece != '':
        uci = uci + promoted_piece.lower()

    # get next player move
    if piece_position[first_key].islower():
        color = 'b'
    elif piece_position[first_key].isupper():
        color = 'w'

    return uci, color, piece

# only checks if King and Rook have empty spaces inbetween
def check_castling(curr_board:str):
    castling = ''

    # white
    if (curr_board[57] == '.') & (curr_board[58] == '.') & ((curr_board[59] == '.')):
        castling = castling + 'K'
    if (curr_board[61] == '.') & (curr_board[62] == '.'):
        castling = castling + 'Q'

    # black
    if (curr_board[5] == '.') & (curr_board[6] == '.'):
        castling = castling + 'k'
    if (curr_board[1] == '.') & (curr_board[2] == '.') & ((curr_board[3] == '.')):
        castling = castling + 'q'

    return castling

# converts uci into index number from 0-63
def get_index(ucihalf:str):
    col = next((key for key, value in cols.items() if value == ucihalf[0]), None)+1
    row = int(ucihalf[1])
    index = col * row - 1

    return index

def check_enpassant(uci:str, piece:str, curr_move:Moves, color:str):

    # check first if it's a pawn move
    if (piece != 'p') & (piece != 'P'):
        return '-'
    
    old_pos = uci[0:2]
    new_pos = uci[2:4]
    enpassant = ''

    # Find the key for the given value
    index = get_index(new_pos)

    if color == 'b':
        if (curr_move.board[index-1] == 'P') | (curr_move.board[index+1] == 'P'):
            enpassant = enpassant + uci[2] + str(int(uci[3])+1)
            return enpassant
    elif color == 'w':
        if (curr_move.board[index-1] == 'p') | (curr_move.board[index+1] == 'p'):
            enpassant = enpassant + uci[2] + str(int(uci[3])-1)
            return enpassant
    else:
        return '-'

# get move list based on lobby id
def get_movelist(curr_move:Moves, table_moves:list[Moves]):
    
    movelist = []
    
    for move in table_moves:
        if move.lobby_id == curr_move.lobby_id:
            movelist.append(move)

    return movelist

def sunfish_to_FEN(board:str):
    parsed = "" # stores parsed board
    point_ctr = 0 # stores no. of empty spaces
    i = 0
    while i < len(board):
        # check if current position is a piece
        if board[i] != '.':
            # appends the number once counter reaches end of empty spaces
            if (board[i - 1] == '.') & (point_ctr > 0):
                parsed = parsed + str(point_ctr)
                point_ctr = 0
                parsed = parsed + board[i]
            else:
                parsed = parsed + board[i]
        # check if current position is empty
        elif board[i] == '.':
            point_ctr+=1
        i+=1

        # if reaches the end of the row
        if i%8 == 0:
            # places stored point_ctr in fen as it reached end of row
            if point_ctr > 0:
                parsed = parsed + str(point_ctr)
                point_ctr = 0
            # doesn't place / as last character
            if i < 64:
                parsed = parsed + '/'
    return(parsed)


# For internal testing only
# def main():

#     zero_move = Moves(moves_id=0, lobby_id=1, board=(
#     "rnbqkbnr"
#     "pppppppp"
#     "........"
#     "........"
#     "......."
#     "........"
#     "PPPPPPPP"
#     "RNBQKBNR"
#     ))
#     first_move = Moves(moves_id=1, lobby_id=1, board=(
#     "rnbqkbnr"
#     "pppppppp"
#     "........"
#     "........"
#     "....P..."
#     "........"
#     "PPPP.PPP"
#     "RNBQKBNR"
#     ))
#     second_move = Moves(moves_id=2, lobby_id=1, board=(
#     "rnbqkbnr"
#     "ppp.pppp"
#     "........"
#     "...p...."
#     "....P..."
#     "........"
#     "PPPP.PPP"
#     "RNBQKBNR"
#     ))
#     third_move = Moves(moves_id=3, lobby_id=1, board=(
#     "r...k..r"
#     "ppp.pppp"
#     "........"
#     "...pP..."
#     "........"
#     "........"
#     "PPPP.PPP"
#     "R..QK..R"
#     ))
#     fourth_move = Moves(moves_id=4, lobby_id=1, board=(
#     "r...k..r"
#     "ppp.p.pp"
#     "........"
#     "...pPp.."
#     "........"
#     "........"
#     "PPPP.PPP"
#     "R..QK..R"
#     ))
#     fifth_move = Moves(moves_id=5, lobby_id=1, board=(
#     "rnbqkbnr"
#     "ppp.p.pp"
#     ".....P.."
#     "...p...."
#     "........"
#     "........"
#     "PPPP.PPP"
#     "RNBQKBNR"
#     ))

#     table_moves = [zero_move, first_move, second_move, third_move, fourth_move, fifth_move]

#     # FEN Format: board_state, color, castling, enpassant, halfmove, fullmove
#     board_state = ''
#     color = ''
#     castling = ''
#     enpassant = '-'
#     halfmove = 0
#     fullmove = 1
#     parsed_FEN = ''

#     board_state = sunfish_to_FEN(third_move.board) 

#     uci, color, piece = get_uci(third_move.board, fourth_move.board)
#     print(uci, color, piece)

#     enpassant = check_enpassant(uci, piece, fourth_move, color)
#     print(enpassant)

#     castling = check_castling(fourth_move.board)
#     print(castling)

#     parsed_FEN = (f'{board_state} {color} {castling} {enpassant} {halfmove} {fullmove}')
#     print(parsed_FEN)

#     board = chess.Board(fen=parsed_FEN)
#     if not board.is_valid():
#         print('error')

#     # checks if move is valid
#     move = chess.Move.from_uci(uci)
#     print(board.legal_moves)
#     print(move in board.legal_moves)

#     return 0

# main()