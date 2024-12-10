import matplotlib.pyplot as plt
import numpy as np
from data import tree_flammability
from data import tree_burn_rates
from plot import plot_fire
from scipy.ndimage import distance_transform_edt

def calculate_humidity_and_temperature(grid):
    rows, cols = grid.shape
    humidities = np.full((rows, cols), 0.1)  # Initialize humidity grid with 20% (0.2) for all cells
    temperatures = np.full((rows, cols), 30)  # Initialize temperature grid with 25°C

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
                        if distance <= 4 and grid[x, y] != 2 and humidities[x, y] < 1:  # Exclude fire cells
                            humidities[x, y] += 0.8 / (distance + 3)  # Decay humidity with distance
                            if humidities[x, y] >= 0.85:
                                humidities[x, y] = 0.85

    # Update temperature based on proximity to fire (grid value 2)
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 2:  # Fire cell
                for x in range(max(0, i - 1), min(rows, i + 2)):  # Check 3x3 area around fire
                    for y in range(max(0, j - 1), min(cols, j + 2)):
                        temperatures[x, y] = min(100,
                                                 temperatures[x, y] + 5)  # Increase temperature by 5, capped at 100°C

    # Adjust temperature based on humidity (e.g., cooler near water, warmer near fire)
    for i in range(rows):
        for j in range(cols):
            if humidities[i, j] > 0.7:  # Near water
                temperatures[i, j] = max(temperatures[i, j] - 2, 0)  # Reduce temperature if near water
            elif humidities[i, j] < 0.3:  # Dry areas (near fire)
                temperatures[i, j] = min(temperatures[i, j] + 2, 100)  # Increase temperature in dry areas

    return humidities, temperatures  # Return both the humidity and temperature grids


def simulate_fire(grid, tree_types, wind_speed, wind_direction, simulations=40):
    rows, cols = grid.shape
    burn_counts = np.zeros_like(grid, dtype=float)  # Tracks burn occurrences for each cell
    hours = 0

    # Set wind speed and direction weights
    if wind_speed < 1:
        tailwind = 1
        against_wind = 1
    else:
        tailwind = 0.49 * wind_speed + 0.5
        against_wind = 1 - tailwind

    wind_weights = {
        'N': [against_wind, tailwind, 1, 1],  # North
        'E': [1, 1, tailwind, against_wind],  # East
        'S': [tailwind, against_wind, 1, 1],  # South
        'W': [1, 1, against_wind, tailwind],  # West
    }
    NZ = wind_weights[wind_direction]

    for sim in range(simulations):
        grid_copy = grid.copy()
        cooldowns = np.zeros_like(grid, dtype=float)
        hours = 0

        while True:
            if np.sum(grid_copy == 2) == 0:  # No fire left
                print(f"Simulation {sim + 1}/{simulations} completed.")
                break

            # Update humidity and temperature
            humidities, temperatures = calculate_humidity_and_temperature(grid_copy)
            new_grid = grid_copy.copy()

            for r in range(rows):
                for c in range(cols):
                    if grid_copy[r, c] == 2 and cooldowns[r, c] <= 0:  # Spread fire
                        for i, (dr, dc) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):  # N, S, W, E
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and (grid_copy[nr, nc] == 1 or grid_copy[nr, nc] == 5):
                                tree_type = tree_types[nr, nc]
                                flammability = tree_flammability[tree_type]
                                burn_rate = tree_burn_rates[tree_type]

                                wind_factor = NZ[i]
                                adjusted_burn_rate = burn_rate * (1 + 0.5 * wind_speed * wind_factor)
                                burn_probability = flammability * (1 - humidities[nr, nc]) * (
                                    1 + (temperatures[nr, nc] - 25) / 100)

                                if np.random.random() < burn_probability:
                                    new_grid[nr, nc] = 2  # Ignite cell
                                    cooldowns[nr, nc] = 1 / adjusted_burn_rate

                        # Burned-out state
                        new_grid[r, c] = 4
                        burn_counts[r,c] += 1
                        cooldowns[r, c] = 0

            cooldowns = np.maximum(0, cooldowns - 1)
            grid_copy = new_grid
            plot_fire(grid_copy, tree_types, hours)
            hours += 1

    # Calculate burn probabilities
    burn_probabilities = burn_counts / simulations
    return burn_probabilities
