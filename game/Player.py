import math

LVL_1 = 2 # only 1 unit (king)
LVL_2 = LVL_1 + 2 # 2 units (including king)
LVL_3 = LVL_2 + 6
LVL_4 = LVL_3 + 10
LVL_5 = LVL_4 + 20
LVL_6 = LVL_5 + 36

INTEREST_THRESHHOLD = 5
MAX_INTEREST = 5

KING_ID = 0
PAWN_ID = 1
BISHOP_ID = 2
KNIGHT_ID = 3
ROOK_ID = 4
QUEEN_ID = 5

BOARD_COLS = 5
BOARD_ROWS = 8

class Player:
    def __init__(self):
        self.money = 0
        self.xp = 0
        self.board = ("_," * (math.floor(BOARD_COLS * BOARD_ROWS / 2) - 1)) + "K"
        self.hp = 42 # answer to life, the universe, everything
        
    # returns LEVEL, CURRENT XP        
    def get_level(self):
        if self.xp < LVL_1:
            return 0, self.xp
        elif self.xp < LVL_2:
            return 1, self.xp % LVL_2
        elif self.xp < LVL_3:
            return 2, self.xp % LVL_3
        elif self.xp < LVL_4:
            return 3, self.xp % LVL_4
        elif self.xp < LVL_5:
            return 4, self.xp % LVL_5
        elif self.xp < LVL_6:
            return 5, self.xp % LVL_6
        elif self.xp >= LVL_6:
            return 6, 0
        else:
            print("ERR: XP INVALID")
            return -1, -1
        
    def buy_xp(self):
        self.xp += 4
        
    def earn_interest(self):
        self.money += min(math.floor(self.money / INTEREST_THRESHHOLD), MAX_INTEREST)
        
    def buy_unit(self, unit):
        if unit == PAWN_ID:
            unit_char = "P"
        elif unit == BISHOP_ID:
            unit_char = "B"
        elif unit == KNIGHT_ID:
            unit_char = "N"
        elif unit == ROOK_ID:
            unit_char = "R"
        elif unit == QUEEN_ID:
            unit_char = "Q"
        else:
            print("ERR: invalid unit id.")
        
        unit_pos = self.board.find(unit_char)
        
        if unit_pos == -1:
            self.board = self.board.replace("_", unit_char, 1)
        else:
            self.board = self.board[unit_pos:] + "*" + self.board[:unit_pos]

    def update_board(self, new_board):
        self.board = new_board

    def print_board(self):
        col = 0
        row = 0
        i = 0
        print("Board State:")
        while i < len(self.board):
            if self.board[i] == "*":
                print(self.board[i], end="")
            elif self.board[i] == ",":
                pass
            elif col + 1 == BOARD_COLS:
                col = 0
                print(self.board[i], end="\n")
                row += 1
            else:
                    print(self.board[i], end=" | ")
                    col += 1

            # update counter
            i += 1

# player = Player()
# player.print_board()