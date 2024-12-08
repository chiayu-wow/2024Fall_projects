import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from src.seeds import initialize_grid
from simulate import simulate_fire, calculate_humidity_and_temperature

# 主程式
if __name__ == "__main__":
    rows, cols = 50,50  # 網格尺寸
    '''
    grid, tree_types = initialize_grid(rows, cols, 0.05)

    with open("data_grid.txt", "w") as file:
        for row in grid:
            file.write(" ".join(map(str, row)) + "\n")

    with open("data_tree_types.txt", "w") as file:
        for row in tree_types:
            file.write(" ".join(map(lambda x: str(x) if x is not None else "None", row)) + "\n")
    '''

    with open('data_grid.txt', 'r') as file:
        data = file.readlines()

    grid = np.array([list(map(int, line.split())) for line in data])

    with open('data_tree_types.txt', 'r') as file:
        data = file.readlines()

    tree_types = np.array([line.split() for line in data])
    # Replace 'None' strings with `None` objects or np.nan (if needed for numerical operations)
    tree_types = np.where(tree_types == 'None', None, tree_types)

    simulate_fire(grid, tree_types, 50, 0.5, 'E')
