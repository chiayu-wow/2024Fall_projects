import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

color_map = {
    0: "brown",  # 未種植
    1: "green",  # 樹木
    2: "red",    # 火焰
    3: "blue",   # 水體
    4: "black"   # 燃燒後
}

# 樹木顏色映射
tree_colors = {
    "pine": "green",  # 松樹為綠色
    "oak": "darkgreen",  # 橡樹為深綠色
    "palm": "yellowgreen"  # 棕櫚樹為黃綠色
}

def plot_fire(grid, tree_types, step):
    # 更新火災顯示
    rows, cols = grid.shape
    grid_colored = np.zeros((rows, cols), dtype=int)  # 默認為未種植區域顏色

    # 替換樹木顏色
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:  # 樹木
                tree_type = tree_types[r, c]  # 獲取該位置的樹種
                grid_colored[r, c] = 1  # 假設樹木為綠色
            elif grid[r, c] == 3:  # 水體區域
                grid_colored[r, c] = 2  # 設置水體區域為藍色
            elif grid[r, c] == 2:  # 火焰
                grid_colored[r, c] = 3  # 火焰區域為紅色
            elif grid[r, c] == 4:  # 燃燒後的區域
                grid_colored[r, c] = 4  # 黑色

    # 自定義顏色映射
    colors = ["brown", "green", "blue", "red", "black"]  # 代表樹木、水體、火焰和燃燒區域的顏色
    cmap = ListedColormap(colors)

    plt.imshow(grid_colored, cmap=cmap, interpolation='nearest')
    plt.colorbar(ticks=[0, 1, 2, 3, 4], label="Cell Type")
    plt.title(f"Fire Spread Simulation - Step {step}")
    plt.pause(0.5)
    plt.clf()