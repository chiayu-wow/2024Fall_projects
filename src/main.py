import numpy as np
from simulate import  simulate_fire
from seeds import initialize_grid
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# 主程式
if __name__ == "__main__":
    rows, cols = 20, 20  # 網格尺寸
    grid, tree_types = initialize_grid(rows, cols)
    simulate_fire(grid, tree_types, steps=20)