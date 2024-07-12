main loop
- preparation round
- - buy units
- - move units
- - buy XP - defines max number of units
- battle round
- - auto battler

game state storage
- 1 line string

state table
- stateID | gameID | round_num(int) | p1_xp | p1_money | p2_xp | p2_money | p3_xp | p3_money | p4_xp | p4_money | p1_board | p2_board | p3_board | p4_board

game table - for each lobby created, initialize with gameID and p1_id. 4 board column and 4 pos column data are to record the end of the game (updated whenever a player loses) - player id is added each time a player joins the lobby, and is the account id
- gameID | p1_id | p2_id | p3_id | p4_id | p1_board | p2_board | p3_board | p4_board | p1_pos | p2_pos | p3_pos | p4_pos

*ADDITIONAL FEATURE: PREFERRED COLOR - player gets to list their top 4 preference on color, and they get the color they want depending on player # priority per game - works like amongus but automated

pawn - smol cat
bishop - reading cat
knight - lucky cat
rook - le choncc
queen - hoodie cat
king - eepy cat

player colors:
beige - pink border
orange - red border
light blue - light blue border
dark blue - yellow border

auto battler
- sunfish

number of pieces at a given point
2 * player level

MONEY & HP MECHANICS
- on win, earn money equivalent to number of pieces left on the board
- on loss, lose hp and earn money equivalent to number of pieces left on the board