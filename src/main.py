import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from src.seeds import initialize_grid


from simulate import  simulate_fire ,calculate_humidity_and_temperature

from data import  grid, tree_types

# 主程式
if __name__ == "__main__":

    rows, cols = 20, 20  # 網格尺寸

    #initialize_grid(rows, cols, 0.05)
    simulate_fire(grid, tree_types,20, 10 , 'S')

