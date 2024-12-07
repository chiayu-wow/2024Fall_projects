from plot import plot_fire
import  matplotlib.pyplot as plt
import numpy as np
from data import  tree_flammability
from data import  tree_colors
from plot import plot_fire

import numpy as np

def calculate_humidity_and_temperature(grid):
    rows, cols = grid.shape
    humidities = np.full((rows, cols), 0.2)  # Initialize humidity grid with 20% (0.2) for all cells
    temperatures = np.full((rows, cols), 25)  # Initialize temperature grid with 25°C

    # Update humidity based on proximity to water (grid value 3)
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 3:  # Water cell
                humidities[i, j] = 0.8  # Set humidity to 0.8 for water cells
                for x in range(rows):
                    for y in range(cols):
                        if grid[x, y] == 3:
                            continue  # Skip other water cells
                        distance = abs(i - x) + abs(j - y)  # Calculate Manhattan distance
                        # Only affect cells within 4 distance of water cells, and avoid fire cells
                        if distance <= 4 and grid[x, y] != 2:  # Exclude fire cells
                            humidities[x, y] += 0.8 / (distance + 2)  # Decay humidity with distance

    # Update temperature based on proximity to fire (grid value 2)
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 2:  # Fire cell
                for x in range(max(0, i - 1), min(rows, i + 2)):  # Check 3x3 area around fire
                    for y in range(max(0, j - 1), min(cols, j + 2)):
                        temperatures[x, y] = min(100, temperatures[x, y] + 5)  # Increase temperature by 5, capped at 100°C

    # Adjust temperature based on humidity (e.g., cooler near water, warmer near fire)
    for i in range(rows):
        for j in range(cols):
            if humidities[i, j] > 0.7:  # Near water
                temperatures[i, j] = max(temperatures[i, j] - 2, 0)  # Reduce temperature if near water
            elif humidities[i, j] < 0.3:  # Dry areas (near fire)
                temperatures[i, j] = min(temperatures[i, j] + 2, 100)  # Increase temperature in dry areas

    return humidities, temperatures  # Return both the humidity and temperature grids


def simulate_fire(grid, tree_types, steps, wind_speed, wind_direction):
    rows, cols = grid.shape
    # 根據風速計算風的影響權重
    if wind_speed < 0.3:
        tailwind = 1
        against_wind = 1
    else:
        tailwind = 0.49 * wind_speed + 0.5
        against_wind = 1 - tailwind
        # 定義風向對應的權重
        # [北、南、西、東]
    wind_weights = {
        'N': [against_wind, tailwind, 1, 1],  # 北
        'E': [1, 1, tailwind, against_wind],  # 東
        'S': [tailwind, against_wind, 1, 1],  # 南
        'W': [1, 1, against_wind, tailwind],  # 西
    }
    NZ = wind_weights[wind_direction]

    for step in range(steps):
        # 檢查是否還有火災，如果沒有，結束模擬
        if np.sum(grid == 2) == 0:
            print("No fire left, ending simulation.")
            break

        # Update humidity and temperature grids before spreading the fire
        humidities, temperatures = calculate_humidity_and_temperature(grid)

        new_grid = grid.copy()
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == 2:  # 火焰擴散
                    # 燃燒鄰近的樹木
                    for i, (dr, dc) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):  # N, S, W, E
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1:
                            # 根據樹種的可燃性和濕氣決定是否燃燒
                            tree_type = tree_types[nr, nc]
                            flammability = tree_flammability[tree_type]
                            # 根據濕氣減少燃燒機率，並考慮溫度的影響
                            burn_probability = flammability * (1 - humidities[nr, nc]) * (
                                        1 + (temperatures[nr, nc] - 25) / 100)
                            # 根據風向調整燃燒機率
                            adjusted_burn_probability = burn_probability * NZ[i]
                            if np.random.random() < adjusted_burn_probability:  # 濕氣越高，燃燒機率越低
                                new_grid[nr, nc] = 2
                    # 燃燒後的區域變為黑色
                    new_grid[r, c] = 4
        grid = new_grid
        plot_fire(grid, tree_types, step)  # 更新並顯示新步驟

    plt.show()