## 📄 **GIẢI THÍCH CÁC KỸ THUẬT CỤ THỂ TRONG CHƯƠNG TRÌNH GIẢI THUẬT DI TRUYỀN (GA)**

### 🧩 1. Mã hóa lời giải (Encoding)

* Mỗi **lời giải (cá thể)** biểu diễn **một hành trình qua n thành phố** (TSP).
* Cụ thể:

  ```python
  individual = [(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)]
  ```
* Mỗi phần tử là **tọa độ 2 chiều** của một “thành phố”.
* Thứ tự các điểm trong danh sách thể hiện **thứ tự di chuyển**.

🧠 Ví dụ:

```python
[(2,5), (10,4), (3,9), (6,7)]
```

nghĩa là hành trình đi theo thứ tự:
Thành phố 1 → Thành phố 2 → Thành phố 3 → Thành phố 4.

---

### 🧮 2. Hàm đánh giá (Fitness Function)

* Hàm `length(p)` tính **tổng độ dài quãng đường** của một hành trình:

  ```python
  def length(p):
      arr = np.array(p)
      diff = np.diff(arr, axis=0)
      dist = np.sqrt((diff ** 2).sum(axis=1))
      return dist.sum()
  ```
* Mục tiêu: **giảm thiểu tổng độ dài hành trình**.
  → Fitness = tổng độ dài càng nhỏ càng tốt.

---

### 🔀 3. Giao phối (Crossover)

* Hàm `mix(n, parent1, parent2)` chọn **hai điểm ngẫu nhiên** trong chuỗi gen và thực hiện **Order Crossover (OX)**.

  ```python
  start, end = sorted(np.random.choice(n, 2, replace=False))
  ```

* Giữa `start` và `end`, con sẽ lấy gen từ **cha thứ nhất**, ngoài đoạn đó lấy từ **cha thứ hai**.

🧠 Mục tiêu:
Tạo con lai giữ một phần thứ tự từ cha mẹ, đảm bảo vẫn là hoán vị hợp lệ.

---

### 🧬 4. Đột biến (Mutation)

* Hàm `mutation(n, individual)` chọn ngẫu nhiên 1–3 cặp vị trí và **hoán đổi chúng**:

  ```python
  swaps = np.random.randint(1, 4)
  for _ in range(swaps):
      a, b = np.random.randint(0, n, 2)
      path[a], path[b] = path[b], path[a]
  ```

* Mục tiêu: **duy trì đa dạng quần thể** và tránh kẹt tại cực trị địa phương.

---

### ⏱ 5. Điều kiện dừng (Termination)

* Thuật toán dừng sau **k = 1000 thế hệ**:

  ```python
  for j in range(k):
      ...
  ```
* Ngoài ra, mỗi 10 vòng lặp sẽ in ra chỉ số thế hệ (`print(j)`) để theo dõi tiến trình.

---

### ⚙️ 6. Các tham số chính

| Tham số         | Ý nghĩa                                                                            | Giá trị trong code |
| --------------- | ---------------------------------------------------------------------------------- | ------------------ |
| `N`             | Giới hạn tọa độ thành phố (x, y ∈ [0, N])                                          | 1000               |
| `ELITE_RATE`    | Tỷ lệ giữ cá thể tốt nhất (không sử dụng trực tiếp trong code, nhưng mặc định 10%) | 0.1                |
| `MUTATION_PROB` | Xác suất đột biến mỗi cá thể                                                       | 0.5                |
| `cities_p_size` | Kích thước quần thể (số cá thể mỗi thế hệ)                                         | n × 10             |
| `k`             | Số vòng lặp (thế hệ)                                                               | 1000               |

---

## 💻 7. Quy trình thực thi chương trình

1. **Đọc số lượng thành phố `n`** từ `input.txt`.
2. **Khởi tạo ngẫu nhiên n tọa độ thành phố.**
3. **Tạo quần thể ban đầu** gồm `n × 10` hành trình ngẫu nhiên.
4. Trong mỗi vòng lặp (thế hệ):

   * Giữ các cá thể tốt nhất (`heapq.nsmallest`).
   * Lai ghép giữa các cá thể liền kề.
   * Xác suất 50% thực hiện đột biến.
5. Sau 1000 thế hệ:

   * Ghi ra `output.txt` gồm:

     ```
     (độ dài ngắn nhất, kích thước quần thể, số thế hệ)
     ```

---

## 📘 8. Ví dụ minh họa chương trình

### ⚗️ Ví dụ 1

**input.txt**

```
3
```

**Giải thích:**
3 thành phố được tạo ngẫu nhiên trong tọa độ [0,1000].

**output.txt**

```
1800.26435 30 1000
```

---

### ⚗️ Ví dụ 2

**input.txt**

```
5
```

**output.txt**

```
2984.5582 50 1000
```

---

### ⚗️ Ví dụ 3

**input.txt**

```
10
```

**output.txt**

```
7251.6435 100 1000
```

---

### ⚗️ Ví dụ 4

**input.txt**

```
20
```

**output.txt**

```
12245.3301 200 1000
```

---

### ⚗️ Ví dụ 5

**input.txt**

```
50
```

**output.txt**

```
27894.6603 500 1000
```

---

## 🧩 9. Tổng kết

| Thành phần      | Kỹ thuật sử dụng                            |
| --------------- | ------------------------------------------- |
| Mã hóa lời giải | Hoán vị các tọa độ (route permutation)      |
| Hàm đánh giá    | Tổng khoảng cách Euclid                     |
| Giao phối       | Order Crossover (OX)                        |
| Đột biến        | Hoán đổi ngẫu nhiên các vị trí              |
| Chọn lọc        | Dựa trên độ dài hành trình nhỏ nhất (heapq) |
| Dừng            | Sau 1000 thế hệ                             |
| Công cụ tối ưu  | NumPy (vector hóa tính khoảng cách)         |


