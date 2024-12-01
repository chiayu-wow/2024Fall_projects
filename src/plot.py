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

# 更新plot_fire函數
def plot_fire(grid, tree_types, step, tree_colors):
    rows, cols = grid.shape

    # 創建grid的顏色映射，初始為未種植區域顏色
    grid_colored = np.zeros((rows, cols), dtype=int)  # 默認為未種植區域（對應數字0）

    # 替換樹木顏色
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:  # 樹木
                tree_type = tree_types[r, c]  # 獲取該位置的樹種
                tree_color = tree_colors.get(tree_type, "green")  # 如果樹種未定義，則使用默認顏色綠色
                # 使用數字來表示樹木顏色
                if tree_color == "green":
                    grid_colored[r, c] = 1
                elif tree_color == "darkgreen":
                    grid_colored[r, c] = 5
                elif tree_color == "yellowgreen":
                    grid_colored[r, c] = 6
            elif grid[r, c] in color_map:  # 如果是火焰或其他特殊區域
                grid_colored[r, c] = grid[r, c]  # 保持原有顏色數字

    # 自定義顏色映射
    colors = ["brown", "green", "red", "blue", "black", "darkgreen", "yellowgreen"]  # 根據需要調整顏色
    cmap = ListedColormap(colors)

    # 使用imshow顯示更新的顏色
    plt.imshow(grid_colored, cmap=cmap, interpolation='nearest')

    # 顯示顏色條
    plt.colorbar(ticks=[0, 1, 2, 3, 4, 5, 6], label="Cell Type")

    # 顯示標題
    plt.title(f"Fire Spread Simulation - Step {step}")

    # 暫停0.5秒，以便查看每個步驟
    plt.pause(0.5)

    # 清除圖像
    plt.clf()