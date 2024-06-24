XP_PER_PURCHASE = 4

KING_ID = 0
PAWN_ID = 1
BISHOP_ID = 2
KNIGHT_ID = 3
ROOK_ID = 4
QUEEN_ID = 5

PAWN_COST = 1
BISHOP_COST = 2
KNIGHT_COST = 2
ROOK_COST = 3
QUEEN_COST = 3

# game state object
class game_state:
    def __init__(self, game_id, round_num, b1_fen, b2_fen):
        self.game_id = game_id
        self.round_num = round_num
        self.b1_fen = b1_fen
        self.b2_fen = b2_fen        

# state table
class db_State:
    def __init__(self):
        self.db = []
        
    def add_state(self, game_state_obj):
        self.db.append(game_state_obj)
        
class game_table_row:
    def __init__(self, game_id, p1_xp, p1_money, p2_xp, p2_money, p3_xp, p3_money, p4_xp, p4_money, p1_board, p2_board, p3_board, p4_board, p1_bench, p2_bench, p3_bench, p4_bench, pawn_count, bishop_count, knight_count, rook_count, queen_count):
        self.game_id = game_id 
        self.p1_xp = p1_xp 
        self.p1_money = p1_money 
        self.p2_xp = p2_xp 
        self.p2_money = p2_money 
        self.p3_xp = p3_xp 
        self.p3_money = p3_money 
        self.p4_xp = p4_xp 
        self.p4_money = p4_money 
        self.p1_board = p1_board 
        self.p2_board = p2_board 
        self.p3_board = p3_board 
        self.p4_board = p4_board 
        self.p1_bench = p1_bench 
        self.p2_bench = p2_bench 
        self.p3_bench = p3_bench 
        self.p4_bench = p4_bench 
        self.pawn_count = pawn_count 
        self.bishop_count = bishop_count 
        self.knight_count = knight_count 
        self.rook_count = rook_count 
        self.queen_count = queen_count

# game table - updates each time an action is made in preparation stage
class db_Game:
    def __init__(self):
        self.db = []
        
    def new_game(self):
        self.db.append(game_table_row)
    
    def update_game(self, game_id):
        for game in self.db:
            if game.game_id == game_id:
                break
        else:
            game = None
            print("ERR: Game not found.")
            return
    
    def buy_xp(self, game_id, player_num):
        for game in self.db:
            if game.game_id == game_id:
                break
        else:
            game = None
            print("ERR: Game not found.")
            return
        
        if player_num == 1:
            game.p1_xp += XP_PER_PURCHASE
        elif player_num == 2:
            game.p2_xp += XP_PER_PURCHASE
        elif player_num == 3:
            game.p3_xp += XP_PER_PURCHASE
        elif player_num == 4:
            game.p4_xp += XP_PER_PURCHASE
        else:
            print("ERR: Invalid player number.")
            
    def update_money(self, game_id, player_num, money_amount):
        for game in self.db:
            if game.game_id == game_id:
                break
        else:
            game = None
            print("ERR: Game not found.")
            return
        
        if player_num == 1:
            game.p1_money += money_amount
        elif player_num == 2:
            game.p2_money += money_amount
        elif player_num == 3:
            game.p3_money += money_amount
        elif player_num == 4:
            game.p4_money += money_amount
        else:
            print("ERR: Invalid player number.")
            
    def buy_unit(self, game_id, player_num, unit_num):
        for game in self.db:
            if game.game_id == game_id:
                break
        else:
            game = None
            print("ERR: Game not found.")
            return
        
        if unit_num == PAWN_ID:
            unit_cost = PAWN_COST
        elif unit_num == BISHOP_ID:
            unit_cost = BISHOP_COST
        elif unit_num == KNIGHT_ID:
            unit_cost = KNIGHT_COST
        elif unit_num == ROOK_ID:
            unit_cost = ROOK_COST
        elif unit_num == QUEEN_ID:
            unit_cost = QUEEN_COST
        else:
            unit_cost = None
            print("ERR: Invalid unit type.")
            return
        
        if player_num == 1:
            game.p1_money -= unit_cost
        elif player_num == 2:
            game.p2_money -= unit_cost
        elif player_num == 3:
            game.p3_money -= unit_cost
        elif player_num == 4:
            game.p4_money -= unit_cost
        else:
            print("ERR: Invalid player number.")
        
        