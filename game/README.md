main loop
- preparation round
- - buy units
- - move units
- - buy XP
- battle round
- - auto battler

game state storage
- 1 line FEN
- - FEN string should indicate 5|5|5|5|5|5|5|5
- - upper case for white, lower case for black
- - \* represents star value of the unit
- - same system will be used for units on a player's bench

state table
- gameID | round_num(int) | b1_fen | b2_fen

game table - used in preparation stage - updates each time an action is made in the prep round
- gameID | p1_xp | p1_money | p2_xp | p2_money | p3_xp | p3_money | p4_xp | p4_money | p1_board | p2_board | p3_board | p4_board | unit(int) | unit(int) | unit(int) | unit(int) | unit(int)

pawn - smol cat
bishop - reading cat
knight - lucky cat
rook - le choncc
queen - hoodie cat
king - eepy cat

team colors:
beige - pink border
orange - red border
light blue - light blue border
dark blue - yellow border

Upgrading mechanic
pawn
- 1* - 1 step forward, eat diagonally
- 2* - randomly become another piece once you reach the end
- 3* - randomly become another piece - happens after round starts, not during prep phase

bishop
- 1* - move diagonally 1 step in all 4 directions
- 2* - move diagonally 3 steps in all 4 directions
- 3* - normal bishop
knight
- 1* - move L to the right only (cannot jump over pieces)
- 2* - move L to both left and right (cannot jump over pieces)
- 3* - normal knight
rook
- 1* - move ordinally 4 steps
- 2* - move ordinally 8 steps
- 3* - normal rook
queen
- 1* - move in all 8 directions 2 steps
- 2* - move in all 8 directions 4 steps
- 3* - normal queen

auto battler
- train via reinforcement learning, or do minimax