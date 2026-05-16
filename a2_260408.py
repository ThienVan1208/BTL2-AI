# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 18:59:30 2021

@author: AZ
"""
import random
import time

def init_board():
    board = [[+1, +1, +1, +1, +1],
             [+1,  0,  0,  0, +1],
             [+1,  0,  0,  0, -1],
             [-1,  0,  0,  0, -1],
             [-1, -1, -1, -1, -1]]
    return board

def copy_board(board):
    new_board = [row[:] for row in board]
    return new_board

def print_board(board):
    for i in range(5):
        for j in range(5):
            if board[4-i][j] == 1:
                print('X', end = ' ')
            elif board[4-i][j] == -1:
                print('O', end = ' ')
            else:
                print('-', end = ' ')
        print()
    print()
    
def dict_neighbors():
    dict_n = {}
    for i in range(5):
        for j in range(5):
            temp = []
            if j == 0:
                temp.append((i, j+1))
            if j == 4:
                temp.append((i, j-1))
            if j > 0 and j < 4:
                temp.append((i, j-1))
                temp.append((i, j+1))
            if i == 0:
                temp.append((i+1, j))
            if i == 4:
                temp.append((i-1, j))
            if i > 0 and i < 4:
                temp.append((i-1, j))
                temp.append((i+1, j))
            if i == j:
                if i == 0:
                    temp.append((i+1, j+1))
                elif i == 4:
                    temp.append((i-1, j-1))
                else:
                    temp.append((i-1, j-1))
                    temp.append((i+1, j+1))
                    temp.append((i+1, j-1))
                    temp.append((i-1, j+1))
            elif i+j == 4:
                if i == 0:
                    temp.append((i+1, j-1))
                elif i == 4:
                    temp.append((i-1, j+1))
                else:
                    temp.append((i-1, j-1))
                    temp.append((i+1, j+1))
                    temp.append((i+1, j-1))
                    temp.append((i-1, j+1))
            if i == 0 and j == 2:
                temp.append((i+1, j-1))
                temp.append((i+1, j+1))
            if i == 4 and j == 2:
                temp.append((i-1, j-1))
                temp.append((i-1, j+1))
            if i == 2 and j == 0:
                temp.append((i+1, j+1))
                temp.append((i-1, j+1))
            if i == 2 and j == 4:
                temp.append((i+1, j-1))
                temp.append((i-1, j-1))
            dict_n[(i,j)] = temp
    return dict_n

dict_nei = dict_neighbors()

# for item in dict_nei:
#     print(item, dict_nei[item])


def get_valid_moves(board, player):
    re = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                start = (i,j)
                nei = dict_nei[start]
                for item in nei:
                    if board[item[0]][item[1]] == 0:
                        re.append((start,item))
    return re

def ngang(board, i , j, enemy):
    ret = []
    if (board[i][j-1] == enemy) and (board[i][j-1] == board[i][j+1]):
        ret.append((i, j-1))
        ret.append((i, j+1)) 
    #print("ngang")
    return ret

def doc(board, i, j, enemy):
    ret = []
    if (board[i+1][j] == enemy) and (board[i+1][j] == board[i-1][j]):
        ret.append((i+1, j))
        ret.append((i-1, j))
    #print("doc")
    return ret

def cheo_1(board, i, j, enemy):
    ret = []
    if (board[i+1][j-1] == enemy) and (board[i+1][j-1] == board[i-1][j+1]):
        ret.append((i+1, j-1))
        ret.append((i-1, j+1))
    #print("cheo_1")
    return ret

def cheo_2(board, i, j, enemy):
    ret = []
    if (board[i+1][j+1] == enemy) and (board[i+1][j+1] == board[i-1][j-1]):
        ret.append((i+1, j+1))
        ret.append((i-1, j-1)) 
    #print("cheo_2")
    return ret
    
def ganh(board, i, j, enemy):
    ret = []
    if (i, j) in [(1, 1), (2, 2), (3, 3), (3, 1), (1, 3)]:
        ret = doc(board, i, j, enemy) + ngang(board, i, j, enemy) + \
                cheo_1(board, i, j, enemy) + cheo_2(board, i, j, enemy)
    if (i, j) in [(2, 1), (2, 3), (1, 2), (3, 2)]:
        ret = doc(board, i, j, enemy) + ngang(board, i, j, enemy)
    if (i, j) in [(0, 1), (0, 2), (0, 3), (4, 1), (4, 2), (4, 3)]:
        ret = ngang(board, i, j, enemy)
    if (i, j) in [(1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4)]:
        ret = doc(board, i, j, enemy)      
    return ret   

def tim_lien_thong(i, j, enemy, board):
    ret = [(i,j)]
    candidates = list(dict_nei[(i,j)])
    for item in candidates:
        if board[item[0]][item[1]] == enemy and item not in ret:
            ret.append(item)
            temp = dict_nei[item]
            for k in temp:
                if k not in candidates:
                    candidates.append(k)
    return ret

def thanh_phan_lien_thong(board, enemy):
    lien_thong = []
    for i in range(5):
        for j in range(5):
            add = True
            if board[i][j] == enemy:
                for l_temp in lien_thong:
                    if (i, j) in l_temp:
                        add = False
                if(add):
                    lien_thong.append(tim_lien_thong(i, j, enemy, board))
    return lien_thong

def tim_khi(tplt, board):
    tap_khi = dict()
    for i in range(len(tplt)):
        item_set = tplt[i]
        temp = []
        for item in item_set:
            neighbors = dict_nei[item]
            for nei in neighbors:
                if nei not in temp and board[nei[0]][nei[1]] == 0:
                    temp.append(nei)
        tap_khi[i] = len(temp)
    return tap_khi
                    

def chet(board, enemy):
    player = -1*enemy
    tplt = thanh_phan_lien_thong(board, enemy)
    khi = tim_khi(tplt, board) 
    ret = False # khong chet duoc
    for i in range(len(khi)):
        if khi[i] == 0:
            ret = True
            for (i, j) in tplt[i]:
                board[i][j] = player
    return ret
            
def act_moves(move, player, board):
    start = move[0]
    end = move[1]
    
    board[start[0]][start[1]] = 0   
    board[end[0]][end[1]] = player
    # ganh
    list_ganh = ganh(board, end[0], end[1], player*-1)
    for item in list_ganh:
        board[item[0]][item[1]] = player
    # chet
    ret2 = chet(board, player*-1)
    # mo
    mo = []
    if len(list_ganh) == 0 and not ret2:
        list_nei = dict_nei[start]
        for item in list_nei:
            if board[item[0]][item[1]] == -1 * player:
                board_copy = copy_board(board)
                move_temp = (item, start)
                ret_temp = ganh(board_copy, start[0], start[1], player)
                if len(ret_temp) > 0:
                    mo.append(move_temp)
    return mo

def npc_move(board, player, mo = None):
    moves = get_valid_moves(board, player)
    if len(moves) == 0:
        return None
    if mo is not None and len(mo) > 0:
        for move in moves:
            if move in mo:
                return move
    index_move = random.randint(0, len(moves) - 1)
    chose_move = moves[index_move]
    for item in moves:
        end = item[1]
        board_copy = copy_board(board)
        enemy = player * (-1)
        l_ganh = ganh(board_copy, end[0], end[1], enemy)
        if len(l_ganh) > 0:
            chose_move = item
            return chose_move

        start = item[0]
        end = item[1]
        board_copy = copy_board(board)
        board_copy[start[0]][start[1]] = 0   
        board_copy[end[0]][end[1]] = player
        if chet(board_copy, -1*player):
            return item
    return chose_move               




# ==================================================
# --- HEURISTIC ---
# ─── Trọng số ────────────────────────────────────────────────
W_PIECE = 100  # mỗi quân hơn/thua
W_MOBILITY = 2  # số nước đi hợp lệ
W_GANH_THREAT = 30  # nguy cơ bị gánh (mỗi quân có thể bị gánh)
W_GANH_OPP = 40  # cơ hội mình gánh đối thủ
W_LIBERTY = 50  # nhóm quân có liberty thấp (nguy cơ chết)
W_CENTER = 3  # kiểm soát vùng trung tâm


# Các ô trung tâm (ưu tiên chiếm giữ)
CENTER_CELLS = {
    (2, 2): 3,
    (1, 1): 2,
    (1, 3): 2,
    (3, 1): 2,
    (3, 3): 2,
    (2, 1): 1,
    (2, 3): 1,
    (1, 2): 1,
    (3, 2): 1,
}


def count_pieces(board, player):
    """Đếm số quân của player và đối thủ."""
    my_count = sum(1 for i in range(5) for j in range(5) if board[i][j] == player)
    op_count = sum(1 for i in range(5) for j in range(5) if board[i][j] == -player)
    return my_count, op_count


def mobility_score(board, player):
    """Số nước đi hợp lệ của mình trừ của đối thủ."""
    my_moves = len(get_valid_moves(board, player))
    op_moves = len(get_valid_moves(board, -player))
    return my_moves - op_moves


def ganh_threat_score(board, player):
    """
    Đánh giá nguy cơ bị đối thủ gánh mình.
    Với mỗi nước đi của đối thủ, thử xem có gánh được quân mình không.
    """
    threat = 0
    enemy = -player
    enemy_moves = get_valid_moves(board, enemy)
    for move in enemy_moves:
        end = move[1]
        board_copy = copy_board(board)
        board_copy[move[0][0]][move[0][1]] = 0
        board_copy[end[0]][end[1]] = enemy
        captured = ganh(board_copy, end[0], end[1], player)
        threat += len(captured) // 2  # mỗi cặp = 1 lần gánh
    return threat


def ganh_opportunity_score(board, player):
    """
    Đánh giá cơ hội mình gánh đối thủ.
    Với mỗi nước đi của mình, thử xem có gánh được không.
    """
    opportunity = 0
    my_moves = get_valid_moves(board, player)
    for move in my_moves:
        end = move[1]
        board_copy = copy_board(board)
        board_copy[move[0][0]][move[0][1]] = 0
        board_copy[end[0]][end[1]] = player
        captured = ganh(board_copy, end[0], end[1], -player)
        opportunity += len(captured) // 2
    return opportunity


def liberty_score(board, player):
    """
    Nhóm quân đối thủ có liberty thấp → sắp chết → tốt cho mình.
    Nhóm quân mình có liberty thấp → nguy hiểm → trừ điểm.
    """
    score = 0

    # Kiểm tra nhóm đối thủ
    enemy_groups = thanh_phan_lien_thong(board, -player)
    enemy_liberties = tim_khi(enemy_groups, board)
    for idx, lib in enemy_liberties.items():
        group_size = len(enemy_groups[idx])
        if lib == 0:
            score += W_LIBERTY * group_size * 2  # nhóm sắp/đã chết
        elif lib == 1:
            score += W_LIBERTY * group_size  # nhóm nguy hiểm
        elif lib == 2:
            score += W_LIBERTY * group_size // 3

    # Kiểm tra nhóm mình
    my_groups = thanh_phan_lien_thong(board, player)
    my_liberties = tim_khi(my_groups, board)
    for idx, lib in my_liberties.items():
        group_size = len(my_groups[idx])
        if lib == 0:
            score -= W_LIBERTY * group_size * 2
        elif lib == 1:
            score -= W_LIBERTY * group_size
        elif lib == 2:
            score -= W_LIBERTY * group_size // 3

    return score


def center_control_score(board, player):
    """Quân ở vị trí trung tâm được cộng điểm."""
    score = 0
    for (i, j), weight in CENTER_CELLS.items():
        if board[i][j] == player:
            score += weight
        elif board[i][j] == -player:
            score -= weight
    return score


def evaluate_board(board, player):
    """
    Hàm đánh giá tổng hợp trạng thái bàn cờ.
    Trả về điểm dương = có lợi cho player, âm = bất lợi.
    """
    my_count, op_count = count_pieces(board, player)

    # Thắng/thua tuyệt đối
    if op_count == 0:
        return 999999
    if my_count == 0:
        return -999999

    # Check the moves of 2 players
    my_moves = get_valid_moves(board, player)
    op_moves = get_valid_moves(board, -player)
    my_moves_count = len(my_moves)
    op_moves_count = len(op_moves)
    
    # Win condition by trapping opponent (no valid moves)
    if op_moves_count == 0:
        return 999999
    if my_moves_count == 0:
        return -999999

    score = 0

    # 1. Chênh lệch quân
    score += (my_count - op_count) * W_PIECE

    # 2. Mobility
    score += mobility_score(board, player) * W_MOBILITY

    # 3. Nguy cơ bị gánh (trừ điểm)
    score -= ganh_threat_score(board, player) * W_GANH_THREAT

    # 4. Cơ hội gánh đối thủ (cộng điểm)
    score += ganh_opportunity_score(board, player) * W_GANH_OPP

    # 5. Liberty (nhóm quân sắp chết)
    score += liberty_score(board, player)

    # 6. Kiểm soát trung tâm
    score += center_control_score(board, player) * W_CENTER

    return score


# ==================================================
# --- MINIMAX ---
_last_board = None
_last_move = None

def get_mo_from_state(current_board, player):
    global _last_board, _last_move
    
    # If this is the first turn or state was reset, there's no history to infer from
    if _last_board is None or _last_move is None:
        return []
        
    # Simulate our last move on the last board to get the state right before opponent's move
    intermediate_board = copy_board(_last_board)
    act_moves(_last_move, player, intermediate_board)
    
    empty_to_occ = 0
    occ_to_empty = 0
    opp_start = None
    
    # Compare intermediate board with current board to find exactly where opponent moved from
    for i in range(5):
        for j in range(5):
            if intermediate_board[i][j] == 0 and current_board[i][j] != 0:
                empty_to_occ += 1
            elif intermediate_board[i][j] != 0 and current_board[i][j] == 0:
                occ_to_empty += 1
                opp_start = (i, j)
                
    # If empty cell count change is not exactly 1, the board was reset (e.g. a new game started)
    if empty_to_occ != 1 or occ_to_empty != 1:
        _last_board = None
        _last_move = None
        return []
        
    # Count our pieces before and after opponent's move
    my_pieces_before = sum(1 for row in intermediate_board for cell in row if cell == player)
    my_pieces_after = sum(1 for row in current_board for cell in row if cell == player)
    
    # If opponent captured any of our pieces (Ganh or Chet), the rules state there is no 'mo' trap
    if my_pieces_after < my_pieces_before:
        return []
        
    mo = []
    my_moves = get_valid_moves(current_board, player)
    for m in my_moves:
        # A trap move MUST end at the exact spot the opponent just vacated
        if m[1] == opp_start: 
            board_temp = copy_board(current_board)
            board_temp[m[0][0]][m[0][1]] = 0
            board_temp[m[1][0]][m[1][1]] = player
            
            # Check if this move actually results in a Ganh
            if len(ganh(board_temp, m[1][0], m[1][1], -player)) > 0:
                mo.append(m)
                
    return mo

def minimax_search(board, depth, alpha, beta, maximizing_player, player, start_time, time_limit, forced_moves=None):
    if time.time() - start_time > time_limit:
        # Time out flag return
        return evaluate_board(board, player), None, True

    if depth == 0:
        return evaluate_board(board, player), None, False

    current_turn_player = player if maximizing_player else -player
    valid_moves = get_valid_moves(board, current_turn_player)
    
    # If opponent has set a forced move (mo), filter valid moves to only that move
    if forced_moves:
        valid_moves = [m for m in valid_moves if m in forced_moves]
        if not valid_moves:
            # Fallback if error
            valid_moves = get_valid_moves(board, current_turn_player)
            
    if not valid_moves:
        return evaluate_board(board, player), None, False

    best_move = None
    time_out = False
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            new_board = copy_board(board)
            mo = act_moves(move, current_turn_player, new_board) 
            
            # Recursive call
            eval_score, _, timeout_occurred = minimax_search(new_board, depth - 1, alpha, beta, False, player, start_time, time_limit, mo)
            if timeout_occurred:
                time_out = True
                
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            # Apply alpha-beta pruning
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move, time_out
        
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_board = copy_board(board)
            mo = act_moves(move, current_turn_player, new_board)
            
            eval_score, _, timeout_occurred = minimax_search(new_board, depth - 1, alpha, beta, True, player, start_time, time_limit, mo)
            if timeout_occurred:
                time_out = True
                
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
                
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move, time_out

def move(board, player, remain_time):
    global _last_board, _last_move
    
    start_time = time.time()
    time_limit = min(remain_time, 2.7) 
    
    implicit_mo = get_mo_from_state(board, player)
    
    best_move_overall = None
    
    max_depth = 10 
    for depth in range(1, max_depth + 1):
        score, move_at_depth, timeout_occurred = minimax_search(
            board=board, 
            depth=depth, 
            alpha=float('-inf'), 
            beta=float('inf'), 
            maximizing_player=True, 
            player=player, 
            start_time=start_time, 
            time_limit=time_limit,
            forced_moves=implicit_mo
        )
        
        if move_at_depth:
            best_move_overall = move_at_depth
            
        # if time out occurs, break immediately to return the best move found so far
        if timeout_occurred or time.time() - start_time > time_limit:
            break
            
    # if depth loop ends without finding any move
    if best_move_overall is None:
        valid_moves = get_valid_moves(board, player)
        if valid_moves:
            best_move_overall = valid_moves[0]
            
    # Save the current state for the next turn to infer opponent's move
    _last_board = copy_board(board)
    _last_move = best_move_overall
    
    return best_move_overall

# ==================================================

def count_X(board):
    count = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == 1:
                count = count + 1
    return count

def main2(first = 'X'):
    board = init_board()
    count = 0
    limit = 100
    if first == 'X':
        player = 1
    else:
        player = -1
    mo = []
    while(True):
        count = count + 1
        # print(count)
        print_board(board)
        if(count > limit):
            X_pieces = count_X(board)
            if X_pieces > 8:
                return 1
            elif X_pieces < 8:
                print("So nuoc di ca van vuot 100, va so quan co cua ban < 8")
                return -1
            else:
                print("So nuoc di ca van vuot 100, va so quan co cua ban = 8")
                return 0
        b_copy = copy_board(board)
        if player == -1:
            chose_move = npc_move(board, player, mo)
        else:
            t = time.time()

            """
            CALL MOVE HERE
            """
            chose_move = move(b_copy, player, remain_time=99)

            e = time.time() - t
            print('Minimax di chuyen: ' + str(chose_move) + ' | Nghi khoang: ' + str(round(e, 3)) + 's')
            #################################################
            
            if e > 3.2:
                print("Thoi gian xu ly vuot 3.2 giay")
                return -1
        if chose_move == None:
            if player == 1:
                print("Khong chon duoc nuoc di")
                return -1
            else:
                return 1
        if player == 1 or player == -1:
            if len(mo) > 0:
                # print(mo)
                if chose_move not in mo:
                    print("Nuoc di mo: ", mo)
                    print("Lua chon cua ban: ", chose_move, " sai")
                    return -1
            valid_moves = get_valid_moves(board, player)
            if chose_move not in valid_moves:
                print("Cac nuoc di hop le: ", valid_moves)
                print("Lua chon cua ban: ", chose_move, " sai")
                return -1
        mo = act_moves(chose_move, player, board)
        player = player * -1
        
    return 0          




def test():
    b = init_board()
    print_board(b)
    b[2][2] = 1
    
    print_board(b)
    
    move = ((3, 3), (3, 2))
    ret = act_moves(move, -1, b)
    b[3][1] = 1
    print_board(b)
    print(ret)
    move = ((2, 2), (3, 3))
    ret = act_moves(move, 1, b)
    print_board(b)
    print(ret)


                
                
                
if __name__ == '__main__':
    print(main2())
                
                
            