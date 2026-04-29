import time
from heuristic import evaluate_board
from a2_260408 import get_valid_moves, copy_board, act_moves


import sys

def get_real_mo():
    # Get the 'mo' variable from the call stack of Python to determine if opponent has set a forced move
    try:
        frame = sys._getframe(1)
        while frame:
            if 'mo' in frame.f_locals and isinstance(frame.f_locals['mo'], list):
                return frame.f_locals['mo']
            frame = frame.f_back
    except Exception:
        pass
    return []

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
    start_time = time.time()
    time_limit = min(remain_time, 2.7) 
    
    # Check mo implicitly using the board state itself
    implicit_mo = get_real_mo()
    
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
            
    return best_move_overall
