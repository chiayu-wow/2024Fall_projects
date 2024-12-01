import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
# 自定義顏色映射
def plot_fire(grid, step):
    colors = ["brown", "green", "red", "blue", "black"]  # 未種植、樹木、火焰、水體、燃燒後
    cmap = ListedColormap(colors)
    plt.imshow(grid, cmap=cmap, interpolation='nearest')
    plt.colorbar(ticks=[0, 1, 2, 3, 4], label="Cell Type")
    plt.title(f"Fire Spread Simulation - Step {step}")
    plt.pause(0.5)
    plt.clf()