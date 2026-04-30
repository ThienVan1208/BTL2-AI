Python 3.12.8

How to run:
```bash
python a2_260408.py
```

RULE:
1. Gánh (Carry): When you move a piece of yours *between* two opponent pieces (in a straight line), those two opponent pieces are "carried" and flipped to your color.
2. Vây/Chẹt (Surround/Trap): If an opponent's piece (or group of pieces) is completely surrounded by your pieces and has no valid empty spots (khi) to move to, those pieces are trapped and flipped to your color.
3. Thế cờ Mở (Trap/Open State): This is an intentional trap where a player leaves an open spot, forcing the opponent to perform a "Gánh" on their turn. If this state occurs, the opponent MUST execute the forced move.
4. Win Condition: A player wins by either capturing all 16 pieces or when the opponent has no valid moves left.

CONVENTION:
- Input: `list[list[int]]`
```python
    [[ 1,  1,  1,  1,  1],
     [ 1,  0,  0,  0,  1],
     [ 1,  0,  0,  0, -1],
     [-1,  0,  0,  0, -1],
     [-1, -1, -1, -1, -1]]
```
    * `0` stands for an empty cell.
    * `1` stands for player X pieces.
    * `-1` stands for player O pieces.

- Output: A tuple `(start, end)` representing the selected move, e.g., `((0, 1), (1, 1))`. The first sub-tuple is the starting coordinate, and the second is the ending coordinate.

Minimax with Alpha-Beta Pruning idea:
- Use the Minimax algorithm to explore possible future board states up to a certain depth.
- **Iterative Deepening**: The algorithm gradually increases the search depth (from 1 to 10). If the time limit is reached during a search, it safely aborts and returns the best move found in the previous completed depth.
- Alpha-Beta Pruning is used to cut off branches in the game tree that don't need to be evaluated (because a better move has already been found), dramatically reducing execution time (required to be under 3 seconds per move).
- At maximum depth or when evaluating leaf nodes, a heuristic function calculates the score based on piece advantage, mobility, and board control.
- Time control mechanism: Ensure `time.time() - start_time` is strictly checked during the recursive steps to avoid time-out penalties.
- Forced Move checking: In the root call (or throughout tree), we must check if `get_mo_from_state()` returns forced moves. If it does, we can only explore those specific branches.

- Pseudo code:
```python
def minimax(board, depth, alpha, beta, is_max):
    if timeout or depth == 0 or game_over: 
        return evaluate(board)
        
    valid_moves = get_forced_moves() or get_all_moves()
    
    best_val = -infinity if is_max else +infinity
    for move in valid_moves:
        new_board = apply_move(board, move)
        val = minimax(new_board, depth-1, alpha, beta, not is_max)
        
        best_val = max(best_val, val) if is_max else min(best_val, val)
        
        # Alpha-beta pruning
        if is_max: alpha = max(alpha, best_val)
        else: beta = min(beta, best_val)
        if beta <= alpha: break
        
    return best_val

def move(board):
    valid_moves = get_forced_moves() or get_all_moves()
    best_move = None

    for m in valid_moves:
        if timeout_close: break
        
        val = minimax(apply_move(board, m), depth=3, -inf, +inf, is_max=False)
        if val > best_score:
            best_score = val
            best_move = m
            
    return best_move or random_move
```