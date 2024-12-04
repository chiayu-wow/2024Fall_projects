from plot import plot_fire
import  matplotlib.pyplot as plt
import numpy as np
from data import  tree_flammability
from data import  tree_colors
from plot import plot_fire


def simulate_fire(grid, tree_types, temperatures, humidities, steps):
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
                            # 根據樹種的可燃性和濕氣決定是否燃燒
                            tree_type = tree_types[nr, nc]
                            flammability = tree_flammability[tree_type]
                            # 根據濕氣減少燃燒機率，並考慮溫度的影響
                            burn_probability = flammability * (1 - humidities[nr, nc]) * (1 + (temperatures[nr, nc] - 25) / 100)

                            if np.random.random() < burn_probability:  # 濕氣越高，燃燒機率越低
                                new_grid[nr, nc] = 2
                    # 燃燒後的區域變為黑色
                    new_grid[r, c] = 4
        grid = new_grid
        plot_fire(grid, tree_types, step)  # 更新並顯示新步驟
    plt.show()

