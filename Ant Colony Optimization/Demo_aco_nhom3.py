import numpy as np
import random

# Tính ma trận khoảng cách
def calculate_distance_matrix(coords):
    n = len(coords)
    return np.array([[np.linalg.norm(np.array(coords[i]) - np.array(coords[j])) if i != j else 0 for j in range(n)] for i in range(n)])

# Thuật toán Ant System
def ant_system(coords, n_ants=10, n_iterations=100, alpha=1, beta=2, rho=0.1, Q=100):
    n = len(coords)
    dist_matrix = calculate_distance_matrix(coords)
    pheromone = np.ones((n, n))
    best_path, best_length = None, float('inf')

    for _ in range(n_iterations):
        paths, lengths = [], []

        for _ in range(n_ants):
            path, visited = [random.randint(0, n - 1)], set()
            visited.add(path[0])

            for _ in range(n - 1):
                current = path[-1]
                probs = [(pheromone[current][j]**alpha) * ((1 / dist_matrix[current][j])**beta) if j not in visited else 0 for j in range(n)]
                next_city = random.choices(range(n), weights=probs)[0]
                path.append(next_city)
                visited.add(next_city)
            
            path.append(path[0])
            length = sum(dist_matrix[path[i]][path[i + 1]] for i in range(n))
            paths.append(path)
            lengths.append(length)

        min_length = min(lengths)
        if min_length < best_length:
            best_length = min_length
            best_path = paths[lengths.index(min_length)]

        pheromone *= (1 - rho)
        for path, length in zip(paths, lengths):
            for i in range(n):
                pheromone[path[i]][path[i + 1]] += Q / length

    return best_path, best_length

# Tọa độ các thành phố
coords = [(0, 0), (1, 2), (2, 4), (3, 1), (4, 3)]

# Chạy thuật toán
best_path, best_length = ant_system(coords)
print(f"Lộ trình tốt nhất: {best_path}")
print(f"Chiều dài ngắn nhất: {best_length}")
