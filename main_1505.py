import a2_260408
import time
from importlib import import_module


def main(player_X, player_O):
    player = 1    

    count = 0
    limit = 100
    
    remain_time_X = 99
    remain_time_O = 99
    
    player_1 = import_module(player_X)
    player_2 = import_module(player_O)
    
    mo = []
    
    board = a2_260408.init_board()
    while(True):
        count = count + 1
        print("Luot di thu: ", count)
        print("Luot di cua quan: ", player)

        a2_260408.print_board(board)
        if(count > limit):
            X_pieces = a2_260408.count_X(board)
            if X_pieces > 8:
                return 1
            elif X_pieces < 8:
                print("So nuoc di ca van vuot 100, va so quan co cua ban < 8")
                return -1
            else:
                print("So nuoc di ca van vuot 100, va so quan co cua ban = 8")
                return 0
        b_copy = a2_260408.copy_board(board)
        start_time = time.time()
        if player == -1:
            chose_move = player_2.move(b_copy, player, remain_time_O)
            elapsed_time = time.time() - start_time
            remain_time_O -= elapsed_time
            print("Quan O con thoi gian suy nghi: ", remain_time_O)
            if remain_time_O < 0:
                return 1
        else:
            chose_move = player_1.move(b_copy, player, remain_time_X)
            elapsed_time = time.time() - start_time
            remain_time_X -= elapsed_time
            print("Quan X con thoi gian suy nghi: ", remain_time_X)
            if remain_time_X < 0:
                return -1
            
        if elapsed_time > 3.0:
            print("Thoi gian xu ly vuot 3.0 giay")
            return player * -1
       
        if chose_move == None:
            print("Khong chon duoc nuoc di")
            return player * -1

        if len(mo) > 0:
            if chose_move not in mo:
                print("Nuoc di mo: ", mo)
                print("Lua chon cua ban: ", chose_move, " sai")
                # return -1
                return player * -1
        
        valid_moves = a2_260408.get_valid_moves(board, player)
        if chose_move not in valid_moves:
            print("Cac nuoc di hop le: ", valid_moves)
            print("Lua chon cua ban: ", chose_move, " sai")
            return player * -1
        print("Ban da chon nuoc di: ", chose_move)
        mo = a2_260408.act_moves(chose_move, player, board)
        player = player * -1
        

ret = main('a2_260408', 'random_agent')
print("Chien thang la quan: ", ret)
 
