from math import sqrt
from random import randint, shuffle
import random
import heapq
import copy
import numpy as np

# ================== CÁC THAM SỐ TOÀN CỤC ===================
N = 1000               # Miền tọa độ (0..N-1), tạo ngẫu nhiên các thành phố
ELITE_RATE = 0.1       # Tỉ lệ elite (phần trăm cá thể tốt nhất giữ lại)
MUTATION_PROB = 0.5    # Xác suất đột biến
# ============================================================


def input_data() -> int:
    """
    Đọc số lượng thành phố (n) từ file input.txt.
    File chỉ chứa một số nguyên.
    """
    with open('input.txt','r', encoding='utf8') as f:
        n = int(f.read().strip())
    return n


def outpuy_data(data: tuple) -> None:
    """
    Ghi dữ liệu (tuple) ra file output.txt, cách nhau bởi dấu cách.
    """
    with open('output.txt', mode='w', encoding='utf8') as f:
        s =""
        for i in data:
            s += f'{i} '
        f.write(s)


def length(p: list[tuple]) -> float:
    """
    Tính độ dài đường đi qua toàn bộ thành phố (tour).
    Input: p - danh sách tọa độ [(x,y),...].
    Output: tổng chiều dài (float).
    """
    if not p:
        return 0.0
    arr = np.array(p)
    # Tính chênh lệch giữa các điểm liên tiếp
    diff = np.diff(arr, axis=0)
    # Tính khoảng cách Euclid từng đoạn
    dist = np.sqrt((diff ** 2).sum(axis=1))
    return float(dist.sum())


def mix(n: int, parent1: list, parent2: list) -> list:
    """
    Thực hiện lai ghép (crossover) theo dạng Order Crossover đơn giản.
    Input: 
        - n: số thành phố
        - parent1, parent2: hai cá thể (danh sách thành phố)
    Output:
        - danh sách 2 cá thể con
    """
    start, end = sorted(np.random.choice(n, 2, replace=False))

    def order_crossover(p1, p2):
        child = [None] * n
        # Copy đoạn giữa từ p1
        child[start:end] = p1[start:end]
        # Copy phần còn lại từ p2 (giữ thứ tự)
        child[0:start] = p2[0:start]
        child[end:] = p2[end:]
        return child

    return [order_crossover(parent1, parent2),
            order_crossover(parent2, parent1)]


def mutation(n: int, individual: list) -> list:
    """
    Thực hiện đột biến: hoán đổi 1-3 cặp thành phố trong lộ trình.
    Input: 
        - n: số thành phố
        - individual: [độ dài, path]
    Output:
        - [độ dài mới, path mới sau đột biến]
    """
    path = copy.deepcopy(individual[1])
    swaps = np.random.randint(1, 4)  # số lần hoán đổi
    for _ in range(swaps):
        a, b = np.random.randint(0, n, 2)
        if a == b:
            b = (b + 1) % n
        path[a], path[b] = path[b], path[a]
    return [length(path), path]


def init(n: int) -> tuple:
    """
    Khởi tạo quần thể ban đầu và chạy thuật toán di truyền.
    Các bước:
        1. Sinh ngẫu nhiên n thành phố (tọa độ trong [0,N-1]).
        2. Khởi tạo quần thể ban đầu (cities_p).
        3. Lặp qua k thế hệ:
            - Chọn lọc elite (giữ cá thể tốt nhất).
            - Lai ghép để sinh cá thể mới.
            - Đột biến ngẫu nhiên với xác suất MUTATION_PROB.
            - Tạo quần thể mới.
        4. Trả về tuple (best length, population size, số thế hệ).
    """
    # ----------------- B1: Tạo dữ liệu -----------------
    cities = set()
    while len(cities) != n:
        i, j = np.random.randint(0, N, 2)
        cities.add((i, j))
    cities = list(cities)

    # ----------------- B2: Khởi tạo quần thể -----------------
    cities_p = []  # mỗi phần tử: [độ dài, path]
    cities_p_size = n * 10
    for _ in range(cities_p_size):
        sample = cities[::]
        np.random.shuffle(sample)
        heapq.heappush(cities_p, [length(sample), sample])

    # ----------------- B3: Vòng tiến hóa -----------------
    k = 1000  # số thế hệ
    for j in range(k):
        # Chọn elite
        elite_count = int(cities_p_size * ELITE_RATE)
        cities_p = heapq.nsmallest(elite_count, cities_p, key=lambda x: x[0])

        # Copy elite sang thế hệ mới
        cities_good = copy.deepcopy(cities_p)

        # Sinh thêm cá thể mới qua lai ghép và đột biến
        for i in range(cities_p_size):
            # Lai ghép 2 cá thể (i và i-1)
            chi = mix(n, cities_p[i][1], cities_p[i - 1][1])
            for chi_ in chi:
                heapq.heappush(cities_good, [length(chi_), chi_])
            # Đột biến
            if np.random.random() < MUTATION_PROB:
                heapq.heappush(cities_good, mutation(n, cities_p[i]))

        # Cập nhật quần thể
        cities_p = cities_good

        # In trạng thái mỗi 10 thế hệ
        if j % 10 == 0:
            print("Generation:", j)

    # ----------------- B4: Kết quả -----------------
    return (cities_p[0][0], cities_p_size, k)


if __name__ == "__main__":
    n = input_data()
    data = init(n)
    outpuy_data(data)
