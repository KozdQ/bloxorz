## Bài toán: BLOXORZ

## Cách chạy chương trình


```
  Usage: command line
  python3 main.py <mapMode: num | num-num | all> <isVisual: 0 | 1> <algorithm: DFS | BFS | ASTAR> <benchmark: 0 | 1> <stat: 0 | 1> 
```

Ví dụ 

- Chạy map 01, giải thuật DFS, không benchmark, không stat mode -> output text
```commandline
    python3 main.py 01 0 DFS 0 0
```

- Chạy map 02 đến map 08, giải thuật DFS, không benchmark, không stat mode -> output text
```commandline
    python3 main.py 1-8 0 DFS 0 0
```

- Chạy 33 map, giải thuật DFS, không benchmark, không stat mode -> output text
```commandline
    python3 main.py all 0 DFS 0 0
```


- Xem cách chơi game map 1 trên web bằng giải thuật DFS
  - NOTE: do xác định bằng toạ độ pointer để click màn hình nên chạy được trên máy sinh viên code, nhưng không chắc chạy được trên máy của người khác vì độ phân giải màn hình khác nhau.
```commandline
    python3 main.py 01 1 DFS 0 0
```
  - Tương tự với "**1-8**" và "**all**" (không khuyến khích chơi hết map sẽ chạy khá lâu)

- Gen file benchmark cho giải thuật DFS -> excel file
```commandline
    python3 main.py all 0 DFS 1 0
```

- Chỉ đọc thông số so sánh giữa các map trên giải thuật DFS
```commandline
    python3 main.py all 0 DFS 0 1
```


### Quy ước về input
Nhóm đã thực hiện chơi trò chơi trên trang web, sau đó đúc kết lại được:
- Trò chơi có chính xác 33 màn
- Qua mỗi màn chơi ghi lại vị trí các ô gạch, các ô trống, các ô có chức năng đặc biệt, vị trí bắt đầu của viên gạch 
1x2, trạng thái của nó và vị trí kết thúc thành một mảng các số thông qua một số quy ước đặt biệt sau:
  - 0: Nơi không có viên gạch lát nền nào (trừ vị trí kết thúc)
  - 1: Nơi có viên gạch lát nền màu trắng
  - 2: Nơi có viên gạch lát nền màu cam 
  - 3: Nơi có nút hình tròn
  - 4: Nơi có nút hình tròn (chỉ mở)
  - 5: Nơi có nút hình tròn (chỉ đóng)
  - 6: Nơi có nút X
  - 7: Nơi có nút X (chỉ mở)
  - 8: Nơi có nút vòng tròn
  - 9: Vị trí kết thúc
  - *: Vị trí khối gạch 1x1 nếu tiếp xúc với gạch lát trong khối gạch chính 1x2 
    - (Nghĩa là nếu đứng sẽ là *, ngược lại, nếu nằm sẽ là **)

Từ đó, quy ước về input cho các level, sẽ như sau:

_Dòng đầu tiên_, bao gồm 4 số **X**, **Y**, **x**, **y**, **k** trong đó:
- **X** là chiều cao tối thiếu để chứa các viên gạch của bản đồ.
- **Y** là chiều ngang tối thiểu để chứa các viên gạch của bản đồ.
- **x**, **y** là vị trí toạ độ (cao, ngang) (trên -> xuống, trái -> phải) bắt đầu của khối gạch (mặc định ở đây viên gạch sẽ đứng khi bắt đầu)
- **k** là số các chuỗi số chức năng
- 
_**k** dòng tiếp theo_, mỗi dòng bao gồm một dãy số **x_k**, **y_k**, ... đảm nhiệm một lệnh thực hiện của các nút chức năng:
- **x_k**, **y_k** là vị trí của nút chức năng đó.
- **num_square** là số lượng viên gạch sẽ xuất hiện hoặc biến mất
- **x_k_i** và **y_k_i** là vị trí của viên gạch sẽ xuất hiện và biến mất
- Nút (3, 4, 5, 6, 7) **x_k**, **y_k**, **num_square**, (**x_k_i**, **y_k_i**)* \[, **...**\]
- Ngoài ra 
  - Nút (3, 6) trong trường hợp đóng/mở gạch cố định không thay đổi **l**, (**value**, **x_l_i**, **y_l_i**)*
  - Nút (4, 5, 7) trong trường hợp đóng/mở gạch ngược lại ý nghĩa của nút sẽ có thêm (**x_l_i**, **y_l_i**)*
- Nút (8) **x_k**, **y_k**, **selected**, **x_1**, **y_1**, **x_2**, **y_2**
  - **selected** là 1 hoặc 2, sau khi phân tách thì viên 1 hoặc viên 2 sẽ tiếp tục được điều khiển,
  - **x_1**, **y_1**, **x_2**, **y_2** là vị trí của từng viên sau khi bị tách ra.

_**X** dòng tiếp theo_, mỗi dòng sẽ gồm **Y** số tương ứng với các số được quy ước ở trên.




Ví dụ về input map 01:

```text
6 10 2 2 0
1 1 1 0 0 0 0 0 0 0
1 1 1 1 1 1 0 0 0 0
1 1 1 1 1 1 1 1 1 0
0 1 1 1 1 1 1 1 1 1
0 0 0 0 0 1 1 9 1 1
0 0 0 0 0 0 1 1 1 0
```