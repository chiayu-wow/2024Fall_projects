import numpy as np
from simulate import  simulate_fire
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 初始化網格
def initialize_grid(rows, cols):
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.3, 0.7])  # 30% 未種植，70% 樹木
    water_bodies = np.random.choice([0, 3], size=(rows, cols), p=[0.9, 0.1])  # 10% 水體
    grid = np.maximum(grid, water_bodies)  # 合併水體和地形特徵
    grid[10, 10] = 2  # 火災初始點設為 (10, 10)
    return grid

# 主程式
if __name__ == "__main__":
    rows, cols = 20, 20  # 網格尺寸
    grid = initialize_grid(rows, cols)
    simulate_fire(grid, steps=20)