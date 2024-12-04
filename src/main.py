import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from src.seeds import initialize_grid
from simulate import  simulate_fire

# 主程式
if __name__ == "__main__":

    rows, cols = 20, 20  # 網格尺寸

    grid, tree_types, temperatures, humidities = initialize_grid(rows, cols, 0.05)
    simulate_fire(grid, tree_types, temperatures, humidities, 20)

