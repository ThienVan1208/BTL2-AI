from a2_260408 import (
    dict_nei,
    ganh,
    copy_board,
    get_valid_moves,
    thanh_phan_lien_thong,
    tim_khi,
    chet,
)

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
