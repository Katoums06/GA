from math import sqrt
from random import randint, shuffle
import random
import heapq
import copy
import numpy as np

N = 1000
ELITE_RATE = 0.1
MUTATION_PROB = 0.5

def input_data() -> int:
    with open('input.txt','r', encoding='utf8') as f:
        n = int(f.read().strip())
    return n


def outpuy_data(data: tuple) -> None:
    with open('output.txt', mode='w', encoding='utf8') as f:
        s =""
        for i in data:
            s += f'{i} '
        f.write(s)


def length(p: list[tuple]) -> float:
    if not p:
        return 0.0
    arr = np.array(p)
    diff = np.diff(arr, axis=0)
    dist = np.sqrt((diff ** 2).sum(axis=1))
    return float(dist.sum())

def mix(n: int, parent1: list, parent2: list) -> list:
    start, end = sorted(np.random.choice(n, 2, replace=False))

    def order_crossover(p1, p2):
        child = [None] * n
        child[start:end] = p1[start:end]
        child[0:start] = p2[0:start]
        child[end:] = p2[end:]
        return child

    return [order_crossover(parent1, parent2),
            order_crossover(parent2, parent1)]

def mutation(n: int, individual: list) -> list:
    path = copy.deepcopy(individual[1])
    swaps = np.random.randint(1, 4)
    for _ in range(swaps):
        a, b = np.random.randint(0, n, 2)
        if a == b:
            b = (b + 1) % n
        path[a], path[b] = path[b], path[a]
    return [length(path), path]

def init(n: int) -> tuple:
    cities = set()
    while len(cities) != n:
        i, j = np.random.randint(0, N, 2)
        cities.add((i, j))
    cities = list(cities)

    cities_p = []
    cities_p_size = n*10
    for _ in range(cities_p_size):
        sample = cities[::]
        np.random.shuffle(sample)
        heapq.heappush(cities_p, [length(sample), sample])

    k = 1000
    for j in range(k):
        cities_p = heapq.nsmallest(cities_p_size, cities_p, key=lambda x: x[0])
        cities_good = copy.deepcopy(cities_p)
        for i in range(cities_p_size):
            chi = mix(n, cities_p[i][1], cities_p[i - 1][1])
            for chi_ in chi:
                heapq.heappush(cities_good, [length(chi_), chi_])
            if np.random.random() < MUTATION_PROB:
                heapq.heappush(cities_good, mutation(n, cities_p[i]))
        cities_p = cities_good
        if j%10 == 0:
            print(j)     
    return (cities_p[0][0], cities_p_size, k)
     
        

if __name__ == "__main__":
    n = input_data()
    data = init(n)
    outpuy_data(data)
