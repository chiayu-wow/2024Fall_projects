from plot import plot_fire
import  matplotlib.pyplot as plt
import numpy as np
from data import  tree_flammability
from data import  tree_colors

# 模擬火災蔓延
# 模擬火災蔓延
def simulate_fire(grid, tree_types, steps):
    rows, cols = grid.shape
    for step in range(steps):
        # 檢查是否還有火災，如果沒有，結束模擬
        if np.sum(grid == 2) == 0:
            print("No fire left, ending simulation.")
            break

        new_grid = grid.copy()
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == 2:  # 火焰擴散
                    # 燃燒鄰近的樹木
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1:
                            # 根據樹種的可燃性決定是否燃燒
                            tree_type = tree_types[nr, nc]
                            if np.random.random() < tree_flammability[tree_type]:
                                new_grid[nr, nc] = 2
                    # 燃燒後的區域變為黑色
                    new_grid[r, c] = 4
        grid = new_grid
        plot_fire(grid, tree_types, step,tree_colors)  # 更新並顯示新步驟
    plt.show()
