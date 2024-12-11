import matplotlib.pyplot as plt
import numpy as np
from data import tree_flammability
from data import tree_burn_rates
from plot import plot_fire
import pandas as pd


def calculate_humidity_and_temperature(grid, season=None):
    """
    Calculate humidity and temperature for a given grid based on the season, proximity to water, and fire.

    Parameters:
    -----------
    grid : numpy.ndarray
        A 2D array representing the simulation grid. Cell values:
        - 3: Water
        - 2: Fire
        - Other: Terrain
    season : str, optional
        Season can be 'summer', 'winter', or None (default season).

    Returns:
    --------
    tuple of numpy.ndarray
        - humidities: A 2D array of calculated humidity values.
        - temperatures: A 2D array of calculated temperature values.

     Examples:
    ---------
    >>> import numpy as np
    >>> grid = np.array([[0, 3, 0], [0, 0, 2], [3, 0, 0]])
    >>> humidities, temperatures = calculate_humidity_and_temperature(grid, season='summer')
    >>> humidities  # doctest: +NORMALIZE_WHITESPACE
    array([[0.46      , 0.8       , 0.41428571],
           [0.46      , 0.46      , 0.1       ],
           [0.8       , 0.46      , 0.39333333]])
    >>> temperatures  # doctest: +NORMALIZE_WHITESPACE
    array([[30, 33, 35],
           [30, 35, 37],
           [28, 35, 35]])
    >>> humidities, temperatures = calculate_humidity_and_temperature(grid, season='winter')
    >>> humidities  # doctest: +NORMALIZE_WHITESPACE
    array([[0.76      , 0.8       , 0.71428571],
           [0.76      , 0.76      , 0.4       ],
           [0.8       , 0.76      , 0.69333333]])
    >>> temperatures  # doctest: +NORMALIZE_WHITESPACE
    array([[10, 15, 15],
           [10, 15, 17],
           [10, 15, 17]])
    """
    rows, cols = grid.shape

    if season == 'summer':
        humidities = np.full((rows, cols), 0.1)
        temperatures = np.full((rows, cols), 30)
    elif season == 'winter':
        humidities = np.full((rows, cols), 0.4)
        temperatures = np.full((rows, cols), 12)
    else:
        humidities = np.full((rows, cols), 0.2)
        temperatures = np.full((rows, cols), 24)  # Initialize temperature grid with 25°C

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


def simulate_fire(grid, tree_types, wind_speed, wind_direction, simulations=1, wind_affected=True, season=None):
    """
    Simulates fire spread on a grid considering tree types, wind speed, wind direction, and season.

    Parameters:
    -----------
    grid : numpy.ndarray
        A 2D array representing the simulation grid. Cell values:
        - 0: Empty land
        - 1: Tree (flammable)
        - 2: Fire (burning)
        - 3: Water (non-flammable)
        - 5: Bushes (flammable but with different properties)
    tree_types : numpy.ndarray
        A 2D array of the same shape as `grid`, assigning types to trees and bushes. Examples:
        - Trees: "pine", "oak", "willow"
        - Bushes: "bush"
    wind_speed : float
        Wind speed in km/h. Higher wind speeds accelerate fire spread.
    wind_direction : str
        Wind direction, one of 'N', 'S', 'E', 'W', indicating where the wind is blowing towards.
    simulations : int, optional
        Number of simulation iterations to run. Default is 1.
    wind_affected : bool, optional
        Whether the wind affects fire spread. Default is True.
    season : str, optional
        Season can be 'summer', 'winter', or None. Seasons impact burn probabilities.

    Returns:
    --------
    tuple
        - numpy.ndarray: Burn probabilities grid after the simulations.
        - pandas.DataFrame: Simulation results containing burned area and duration for each simulation.

    Examples:
    ---------
    >>> import numpy as np
    >>> grid = np.array([[0, 1, 2, 3],
    ...                  [1, 1, 0, 3],
    ...                  [0, 2, 1, 0],
    ...                  [3, 0, 0, 1]])
    >>> # Tree types: assign types to trees and bushes
    >>> tree_types = np.empty_like(grid, dtype=object)
    >>> tree_types[grid == 1] = np.random.choice(["pine", "oak", "willow"], size=np.sum(grid == 1))
    >>> tree_types[grid == 5] = "bush"
    >>> wind_speed = 5
    >>> wind_direction = 'N'
    >>> burn_probs, results_df = simulate_fire(grid, tree_types, wind_speed, wind_direction, simulations=1)
    >>> burn_probs.shape
    (4, 4)
    >>> 'burned_area' in results_df.columns
    True
    """
    # Initialize simulation variables
    rows, cols = grid.shape
    burn_counts = np.zeros_like(grid, dtype=float)  # Tracks burn occurrences for each cell
    simulation_results = []  # To store results of each simulation

    # Set wind speed and direction weights
    if wind_speed < 1:
        tailwind = 1
        against_wind = 1
    else:
        tailwind = 0.49 * wind_speed + 0.5
        against_wind = 1 - tailwind

    # Wind effect factors for each direction
    wind_weights = {
        'N': [against_wind, tailwind, 1, 1],  # North
        'E': [1, 1, tailwind, against_wind],  # East
        'S': [tailwind, against_wind, 1, 1],  # South
        'W': [1, 1, against_wind, tailwind],  # West
    }
    NZ = wind_weights[wind_direction]  # Get wind effect based on direction

    for sim in range(simulations):
        grid_copy = grid.copy()  # Copy grid for simulation
        cooldowns = np.zeros_like(grid, dtype=float)  # Initialize cooldown grid
        hours = 0
        total_burned_area = 0  # Tracks the total burned area in this simulation

        while True:
            # Terminate simulation if no fire is left
            if np.sum(grid_copy == 2) == 0:
                break

            # Update humidity and temperature based on the season
            humidities, temperatures = calculate_humidity_and_temperature(grid_copy, season)
            new_grid = grid_copy.copy()

            # Iterate over grid cells to simulate fire spread
            for r in range(rows):
                for c in range(cols):
                    if grid_copy[r, c] == 2 and cooldowns[r, c] <= 0:  # Burning cell
                        # Spread fire to neighboring cells (N, S, W, E)
                        for i, (dr, dc) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and (grid_copy[nr, nc] == 1 or grid_copy[nr, nc] == 5):
                                tree_type = tree_types[nr, nc]  # Get tree type
                                flammability = tree_flammability[tree_type]  # Get flammability rate
                                burn_rate = tree_burn_rates[tree_type]  # Get burn rate

                                wind_factor = NZ[i]  # Get wind factor for this direction

                                # Adjust burn rate based on wind and conditions
                                adjusted_burn_rate = burn_rate * (1 + wind_factor) if wind_affected else burn_rate
                                burn_probability = flammability * (1 - humidities[nr, nc]) * (
                                        1 + (temperatures[nr, nc] - 25) / 100) * (
                                                           1 + wind_factor / 5)

                                # Ignite neighboring cell based on probability
                                if np.random.random() < burn_probability:
                                    new_grid[nr, nc] = 2  # Ignite cell
                                    cooldowns[nr, nc] = 1 / adjusted_burn_rate

                        # Mark current cell as burned out
                        new_grid[r, c] = 4
                        burn_counts[r, c] += 1
                        cooldowns[r, c] = 0
                        total_burned_area += 1  # Increment burned area count

            # Update cooldowns and grid
            cooldowns = np.maximum(0, cooldowns - 1)
            grid_copy = new_grid
            plot_fire(grid_copy, tree_types, hours)  # Visualize fire progression
            hours += 1

        # Store results for this simulation
        simulation_results.append({
            "simulation": sim + 1,
            "burned_area": total_burned_area,
            "duration": hours
        })

    # Convert results to a DataFrame for analysis
    results_df = pd.DataFrame(simulation_results)

    # Calculate burn probabilities
    burn_probabilities = burn_counts / simulations

    # Plot burn probabilities heatmap
    plt.figure(figsize=(10, 5))
    plt.title("Burn Probabilities Heatmap")
    plt.imshow(burn_probabilities, cmap="hot", interpolation="nearest")
    plt.colorbar(label="Burn Probability")
    plt.show()

    return burn_probabilities, results_df
