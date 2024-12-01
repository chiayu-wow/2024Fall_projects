import numpy as np


def initialize_grid(rows, cols):
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.3, 0.7])  # 30% 未種植，70% 樹木
    water_bodies = np.random.choice([0, 3], size=(rows, cols), p=[0.9, 0.1])  # 10% 水體
    grid = np.maximum(grid, water_bodies)  # 合併水體和地形特徵
    grid[10, 10] = 2  # 火災初始點設為 (10, 10)

    # 樹木類型
    tree_types = np.empty_like(grid, dtype=object)
    tree_types[grid == 1] = np.random.choice(["pine", "oak", "palm"], size=np.sum(grid == 1))
    return grid, tree_types