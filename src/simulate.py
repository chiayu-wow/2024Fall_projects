from plot import plot_fire
import  matplotlib.pyplot as plt
# 模擬火災蔓延
def simulate_fire(grid, steps):
    rows, cols = grid.shape
    for step in range(steps):
        new_grid = grid.copy()
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == 2:  # 火焰擴散
                    # 燃燒鄰近的樹木
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1:
                            new_grid[nr, nc] = 2
                    # 燃燒後的區域變為黑色
                    new_grid[r, c] = 4
        grid = new_grid
        plot_fire(grid, step)
    plt.show()