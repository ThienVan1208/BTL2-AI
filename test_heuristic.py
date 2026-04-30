"""
Test nhanh heuristic.py
Chạy: python test_heuristic.py
"""

import sys, os

sys.path.insert(0, os.path.dirname(__file__))

from a2_260408 import init_board, copy_board, print_board, act_moves
from heuristic import evaluate_board

SEP = "=" * 50


def test_initial_board():
    print(SEP)
    print("TEST 1: Bàn cờ ban đầu (phải gần 0 vì cân bằng)")
    board = init_board()
    print_board(board)
    score_p1 = evaluate_board(board, 1)
    score_pm1 = evaluate_board(board, -1)
    print(f"  Player  1 (X) score: {score_p1}")
    print(f"  Player -1 (O) score: {score_pm1}")
    assert abs(score_p1) < 500, "FAIL: điểm ban đầu quá lớn"
    assert abs(score_pm1) < 500, "FAIL: điểm ban đầu quá lớn"
    print("  PASS ✓")


def test_more_pieces():
    print(SEP)
    print("TEST 2: Mình nhiều quân hơn → điểm dương")
    board = init_board()
    # Xóa bớt 3 quân đối thủ (-1)
    board[4][0] = 0
    board[4][1] = 0
    board[4][2] = 0
    print_board(board)
    score = evaluate_board(board, 1)
    print(f"  Player 1 score: {score}")
    assert score > 0, "FAIL: nhiều quân hơn nhưng điểm âm"
    print("  PASS ✓")


def test_fewer_pieces():
    print(SEP)
    print("TEST 3: Mình ít quân hơn → điểm âm")
    board = init_board()
    # Xóa bớt 3 quân mình (1)
    board[0][0] = 0
    board[0][1] = 0
    board[0][2] = 0
    print_board(board)
    score = evaluate_board(board, 1)
    print(f"  Player 1 score: {score}")
    assert score < 0, "FAIL: ít quân hơn nhưng điểm dương"
    print("  PASS ✓")


def test_ganh_opportunity():
    print(SEP)
    print("TEST 4: Có cơ hội gánh → điểm tốt hơn")
    # Tạo bàn cờ mà player 1 có thể gánh -1
    board = [[0] * 5 for _ in range(5)]
    board[2][2] = 1  # quân mình ở giữa
    board[2][0] = -1  # quân địch bên trái
    board[2][4] = -1  # quân địch bên phải
    # player 1 đi (2,2) → (2,1) hoặc (2,3) sẽ kẹp địch
    board[1][2] = 1
    board[3][2] = 1
    print_board(board)
    score = evaluate_board(board, 1)
    print(f"  Player 1 score khi có cơ hội gánh: {score}")
    print("  (không có assert cứng, chỉ xem điểm dương không)")
    print("  PASS ✓")


def test_win_lose():
    print(SEP)
    print("TEST 5: Thắng/thua tuyệt đối")
    board = init_board()
    # Xóa hết quân địch
    for i in range(5):
        for j in range(5):
            if board[i][j] == -1:
                board[i][j] = 0
    score = evaluate_board(board, 1)
    print(f"  Win score (player 1): {score}")
    assert score == 999999, f"FAIL: thắng phải là 999999, nhận được {score}"

    board2 = init_board()
    for i in range(5):
        for j in range(5):
            if board2[i][j] == 1:
                board2[i][j] = 0
    score2 = evaluate_board(board2, 1)
    print(f"  Lose score (player 1): {score2}")
    assert score2 == -999999, f"FAIL: thua phải là -999999, nhận được {score2}"
    print("  PASS ✓")


def test_minimax_returns_move():
    print(SEP)
    print("TEST 6: minimax.move() trả về nước đi hợp lệ")
    try:
        from minimax import move
        from a2_260408 import get_valid_moves

        board = init_board()
        import time

        t = time.time()
        result = move(board, 1, remain_time=99)
        elapsed = time.time() - t
        print(f"  Nước đi trả về: {result}")
        print(f"  Thời gian: {elapsed:.3f}s")
        valid = get_valid_moves(board, 1)
        assert result in valid, f"FAIL: {result} không phải nước đi hợp lệ"
        assert elapsed < 3.2, f"FAIL: quá 3.2 giây ({elapsed:.2f}s)"
        print("  PASS ✓")
    except ImportError as e:
        print(f"  SKIP (không tìm thấy minimax.py): {e}")


if __name__ == "__main__":
    print("\n🧪 BẮT ĐẦU TEST HEURISTIC\n")
    tests = [
        test_initial_board,
        test_more_pieces,
        test_fewer_pieces,
        test_ganh_opportunity,
        test_win_lose,
        test_minimax_returns_move,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {e}")
        except Exception as e:
            print(f"  ❌ LỖI: {e}")
    print(SEP)
    print(f"\n✅ {passed}/{len(tests)} tests passed\n")
