# BÀI TẬP LỚN 2 (HK2 25-26): GAME PLAYING

## Mục tiêu
* [cite_start]Hiện thực các giải thuật game-playing cơ bản như: Minimax, Monte-Carlo Tree Search[cite: 3].
* [cite_start]Hiện thực giải thuật chơi tự động được 1 loại cờ, từ đó có thể áp dụng cho các loại cờ khác[cite: 3].

## Yêu cầu
[cite_start]Trong bài tập lớn này nhóm sinh viên được yêu cầu hiện thực 1 giải thuật để có thể chơi tự động cờ Gánh[cite: 4].

### Luật chơi cờ Gánh (Cờ Chém)
Cờ Gánh là trò chơi chiến thuật dân gian Việt Nam với các quy tắc sau:

1. Bàn cờ và Quân cờ:
* Bàn cờ là một tấm bề mặt phẳng chia thành 25 ô bằng lưới vuông 4x4. Các quân cờ di chuyển theo đường ngang, đứng và đường chéo.
* Mỗi người chơi có 8 quân cờ (tổng cộng 16 quân trên bàn).
* Các quân cờ di chuyển đến một trong những giao điểm lân cận còn trống.

2. Các quy tắc ăn quân:
* Gánh: Khi bạn di chuyển một quân cờ của mình vào giữa hai quân của đối phương (nằm trên một đường thẳng), hai quân đối phương đó bị "gánh" và đổi màu thành quân của bạn.
* Vây/Chẹt: Nếu quân của đối phương bị quân của bạn bao vây hoàn toàn khiến chúng không còn khả năng di chuyển (không còn ô trống xung quanh), các quân đó sẽ bị đổi màu thành quân của bạn.
* Thế cờ Mở (Bẫy): Đây là chiến thuật chủ động để đối phương "gánh" quân của mình. Khi một người chơi tạo thế "mở", đến lượt của đối phương, họ bắt buộc phải thực hiện nước đi "gánh" như đã được gài.

3. Điều kiện thắng:
* Trò chơi kết thúc khi một người chơi chiếm được toàn bộ 16 quân cờ hoặc đối phương không còn nước đi hợp lệ nào.

### [cite_start]Hàm cần viết: move(board, player, remain_time) [cite: 6]

* Input:
    * [cite_start]board: ma trận chứa các số nguyên có kích thước 5x5 thể hiện trạng thái hiện tại của bàn cờ, chứa 1 trong 3 giá trị: 1 là quân 'O', -1 là quân 'X', 0 là ô trống[cite: 7].
      Ví dụ: `board = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, -1], [-1, 0, 0, 0, -1], [-1, -1, -1, -1, -1]]` [cite: 8-21].
    * player: 1 hoặc -1, thể hiện lượt chơi của player nào[cite: 22].
    * remain_time: 99 giây cho mỗi người chơi và sẽ trừ dần sau mỗi nước đi[cite: 23].

* Output: trả về tuple (start, end) với:
    * [cite_start]start: tuple chứa vị trí của quân cờ được chọn để di chuyển[cite: 25].
    * [cite_start]end: tuple chứa vị trí mới của quân cờ được chọn[cite: 26].
    * [cite_start]Ví dụ: di chuyển quân cờ ở vị trí (0, 1) đến vị trí mới là (1, 1) thì kết quả trả về của hàm move là: ((0, 1), (1, 1))[cite: 27, 28].

### Quy định chung
* [cite_start]Thời gian tính toán: tối đa 3 giây cho mỗi nước đi[cite: 30].
* [cite_start]Nhóm: Như bài tập lớn 1 (cần thay đổi thì gửi email cập nhật)[cite: 31, 32].

## Cách đánh giá
[cite_start]BTL được đánh giá qua 2 giai đoạn[cite: 33, 34]:
* [cite_start]Giai đoạn 1 (60% số điểm): đấu với agent chơi ngẫu nhiên 10 ván[cite: 35].
* [cite_start]Giai đoạn 2 (40% số điểm): giải đấu trực tiếp[cite: 36].

## Hạn nộp
* [cite_start]Giai đoạn 1: 23g55 ngày 06/05[cite: 38].
* [cite_start]Giai đoạn 2: Thông báo sau[cite: 39].

## Tham khảo
* [cite_start]Minimax algorithm [cite: 41]
* [cite_start]Alpha-beta pruning [cite: 42]
* [cite_start]Monte-Carlo Tree Search [cite: 43]
* [cite_start]Q-learning [cite: 44]
* [cite_start]AlphaGo [cite: 45]