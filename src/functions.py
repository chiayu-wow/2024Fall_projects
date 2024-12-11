import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt
from plot import create_heatmap, plot_single_heatmap
from simulate import simulate_fire
import numpy as np
import pandas as pd


# Hypothesis 1 functions
def clear_and_set_fire(grid, start_point):
    """
    Clears all fire points and sets a new fire point.

    :param grid: numpy array, simulation grid
    :param start_point: tuple[int, int], fire point coordinates (row, col)
    :return: numpy array, the updated grid with the new fire point

    >>> grid = np.array([[0, 0], [2, 0]])
    >>> clear_and_set_fire(grid, (0, 1))
    array([[0, 2],
           [0, 0]])
    """
    grid_copy = grid.copy()
    grid_copy[grid_copy == 2] = 0  # Clear all potential fire sources
    grid_copy[start_point] = 2  # Set the unique fire point
    return grid_copy


def find_closest_location(grid, tree_types, target_type, center):
    """
    Finds the location of the specified type that is closest to the center.

    :param grid: numpy array, simulation grid
    :param tree_types: numpy array, tree type grid
    :param target_type: str, target type ('bush' or 'non_bush')
    :param center: tuple[int, int], center coordinates (row, col)
    :return: tuple[int, int] or None, the closest location

    >>> grid = np.array([[5, 0], [1, 5]])
    >>> tree_types = np.array([['bush', 'bush'], ['non_bush', 'bush']])
    >>> find_closest_location(grid, tree_types, "bush", center=(0, 0))
    (0, 0)
    """
    if target_type == "bush":
        locations = list(zip(*np.where(grid == 5)))  # Find all Bush locations
    elif target_type == "non_bush":
        locations = list(zip(*np.where((grid == 1) & (tree_types != "bush"))))  # Find all Non-Bush locations
    else:
        raise ValueError("Invalid target_type. Use 'bush' or 'non_bush'.")

    distances = [((loc[0] - center[0]) ** 2 + (loc[1] - center[1]) ** 2, loc) for loc in locations]
    distances.sort(key=lambda x: x[0])

    return distances[0][1] if distances else None


def simulate_multiple_starts(grid, tree_types, start_locations, wind_speed, wind_direction):
    """
    Simulates multiple fire starting points, recording burned area and time for each.

    :param grid: numpy array, simulation grid
    :param tree_types: numpy array, tree type grid
    :param start_locations: list of tuples, list of fire point coordinates
    :param wind_speed: float, wind speed
    :param wind_direction: str, wind direction (N, E, S, W)
    :return: pandas DataFrame, combined results for all simulations

    >>> grid = np.zeros((5, 5))
    >>> tree_types = np.array([['bush'] * 5] * 5)
    >>> start_locations = [(2, 2)]
    >>> simulate_multiple_starts(grid, tree_types, start_locations, wind_speed=1, wind_direction="E").empty
    False
    """
    all_results = []

    for start_point in start_locations:
        grid_with_fire = clear_and_set_fire(grid, start_point)
        _, simulation_results = simulate_fire(grid_with_fire, tree_types, wind_speed, wind_direction, simulations=1)
        all_results.append(simulation_results)
        break

    combined_results = pd.concat(all_results, ignore_index=True)
    return combined_results


def compare_bush_non_bush(grid, tree_types, wind_speed, wind_direction):
    """
    Compares simulation results for fire points starting in bush and non-bush areas.

    :param grid: numpy array, simulation grid
    :param tree_types: numpy array, tree type grid
    :param wind_speed: float, wind speed
    :param wind_direction: str, wind direction (N, E, S, W)
    :return: pandas DataFrame, combined results for Bush and Non-Bush simulations

    >>> grid = np.zeros((5, 5))
    >>> grid[2, 2] = 5  # Bush
    >>> tree_types = np.array([['bush'] * 5] * 5)
    >>> compare_bush_non_bush(grid, tree_types, wind_speed=1, wind_direction="E").empty
    No valid Non-Bush fire point found.
    False
    """
    center_point = (25, 25)
    closest_bush = find_closest_location(grid, tree_types, target_type="bush", center=center_point)
    closest_non_bush = find_closest_location(grid, tree_types, target_type="non_bush", center=center_point)

    results_bush = pd.DataFrame()
    results_non_bush = pd.DataFrame()

    if closest_bush:
        # print(f"Simulating fire point (Bush): {closest_bush}")
        results_bush = simulate_multiple_starts(grid, tree_types, [closest_bush], wind_speed=wind_speed,
                                                wind_direction=wind_direction)
        results_bush["category"] = "fire_at_bush"
    else:
        print("No valid Bush fire point found.")

    if closest_non_bush:
        # print(f"Simulating fire point (Non-Bush): {closest_non_bush}")
        results_non_bush = simulate_multiple_starts(grid, tree_types, [closest_non_bush], wind_speed=wind_speed,
                                                    wind_direction=wind_direction)
        results_non_bush["category"] = "fire_at_non_bush"
    else:
        print("No valid Non-Bush fire point found.")

    combined_results = pd.concat([results_bush, results_non_bush], ignore_index=True)
    return combined_results


# Hypothesis 2 functions
def plot_fire_and_water_influence(grid, burn_probabilities):
    """
    Visualize the relationship between water proximity and burn probabilities in a grid-based fire simulation.

    Parameters:
    -----------
    grid : numpy.ndarray
        A 2D array representing the simulation grid. Each cell has an integer value indicating its type:
        - 3: Water
        - Other values can represent various terrain types (e.g., trees, empty land, etc.).
    burn_probabilities : numpy.ndarray
        A 2D array of the same shape as `grid` containing the burn probabilities for each cell.

    Functionality:
    --------------
    1. Identifies water cells (value 3 in `grid`) and calculates the distance of every cell to the nearest water cell.
    2. Adjusts the burn probabilities based on proximity to water:
       - Burn probabilities decrease with proximity to water, with a maximum influence distance of 5 cells.
    3. Generates visualizations:
       - Heatmap of initial burn probabilities.
       - Heatmap of distances to water.
       - Boxplot comparing burn probabilities of cells close to water (distance ≤ 5) and far from water (distance > 5).

    Returns: None
    """

    water_cells = (grid == 3)

    # Calculate the distance to the nearest water
    distances_to_water = distance_transform_edt(~water_cells)

    # Create visualizations
    # Plot 1: Burn Probabilities Heatmap
    plot_single_heatmap(
        burn_probabilities, "hot", "Burn Probabilities Heatmap", "Column Index", "Row Index", "Burn Probability"
    )

    # Plot 2: Distance to Water Heatmap
    plot_single_heatmap(
        distances_to_water, "cool", "Distance to Water Heatmap", "Column Index", "Row Index",
        "Distance to Water (Cells)"
    )

    # Plot 3: Boxplot and Statistical Analysis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Extract burn probabilities for cells near water (distance ≤ 5 cells) and far from water (distance > 5)
    close_to_water = burn_probabilities[distances_to_water <= 5]
    far_from_water = burn_probabilities[distances_to_water > 5]

    # Boxplot
    ax.boxplot([close_to_water, far_from_water], labels=['Close to Water', 'Far from Water'], showfliers=False)
    ax.set_title("Box Plot of Burn Probabilities")
    ax.set_ylabel("Burn Probability")

    # Calculate and print statistics
    stats_close = {
        'mean': np.mean(close_to_water),
        'median': np.median(close_to_water),
        'std': np.std(close_to_water)
    }

    stats_far = {
        'mean': np.mean(far_from_water),
        'median': np.median(far_from_water),
        'std': np.std(far_from_water)
    }

    print("Statistics for cells close to water (distance ≤ 5 cells):")
    print(f"Mean: {stats_close['mean']:.4f}, Median: {stats_close['median']:.4f}, Std: {stats_close['std']:.4f}")

    print("\nStatistics for cells far from water (distance > 5 cells):")
    print(f"Mean: {stats_far['mean']:.4f}, Median: {stats_far['median']:.4f}, Std: {stats_far['std']:.4f}")

    plt.tight_layout()
    plt.show()


# Hypothesis 3 functions
def compare_wind_speeds(grid, tree_types, wind_speeds, wind_direction):
    """
    Compare simulations under different wind speeds for a given wind direction.

    :param grid: numpy array, simulation grid
    :param tree_types: numpy array, tree type grid
    :param wind_speeds: list of float, wind speeds to test
    :param wind_direction: str, wind direction (e.g., 'N')
    :return: pandas DataFrame, combined results for all wind speed conditions
    """
    all_results = []  # Store results from all conditions

    for wind_speed in wind_speeds:
        print(f"Simulating for wind speed: {wind_speed} m/s, direction: {wind_direction}")

        # Clear and set fire in the middle of the grid
        grid_with_fire = clear_and_set_fire(grid, (grid.shape[0] // 4, grid.shape[1] // 2))

        # Simulate fire
        burn_probabilities, simulation_results = simulate_fire(grid_with_fire, tree_types, wind_speed, wind_direction,
                                                               1)

        # Add wind speed and direction to results
        simulation_results["wind_speed"] = wind_speed
        simulation_results["wind_direction"] = wind_direction

        # Append results to the list
        all_results.append(simulation_results)

    # Combine all results into a single DataFrame
    combined_results = pd.concat(all_results, ignore_index=True)
    return combined_results, burn_probabilities


# Validation functions
def describe_data(data, season):
    """
        Print summary statistics for the given dataset of burn probabilities for a specific season.

        Parameters:
        -----------
        data : numpy.ndarray or list
            The dataset containing burn probabilities. This can be a 1D array or list of numerical values.
        season : str
            The name of the season corresponding to the data (e.g., "spring", "summer", "fall", "winter").
            This is used for labeling the output.

        Functionality:
        --------------
        Computes and prints the following descriptive statistics for the input data:
        - Mean: The average value of the dataset.
        - Standard Deviation: Measure of the spread of the dataset.
        - Minimum Value: The smallest value in the dataset.
        - Maximum Value: The largest value in the dataset.
        - 25th Percentile: The value below which 25% of the data falls.
        - 50th Percentile (Median): The middle value of the dataset.
        - 75th Percentile: The value below which 75% of the data falls.

        Output:
        -------
        Prints the computed statistics to the console, formatted for clarity and labeled with the given season.

        Example:
        --------
        >>> data = [0.1, 0.2, 0.3, 0.4, 0.5]
        >>> describe_data(data, "spring")
        Descriptive Statistics for Spring Season:
        Mean: 0.3000
        Standard Deviation: 0.1414
        Min: 0.1000
        Max: 0.5000
        25th Percentile: 0.2000
        50th Percentile (Median): 0.3000
        75th Percentile: 0.4000
        ----------------------------------------
    """
    print(f"Descriptive Statistics for {season.capitalize()} Season:")
    print(f"Mean: {np.mean(data):.4f}")
    print(f"Standard Deviation: {np.std(data):.4f}")
    print(f"Min: {np.min(data):.4f}")
    print(f"Max: {np.max(data):.4f}")
    print(f"25th Percentile: {np.percentile(data, 25):.4f}")
    print(f"50th Percentile (Median): {np.percentile(data, 50):.4f}")
    print(f"75th Percentile: {np.percentile(data, 75):.4f}")
    print("-" * 40)


def plot_heatmap_and_boxplot(winter_data, summer_data, grid_size=(50, 50)):
    """
    Plots a heatmap of burn probabilities for winter and summer seasons, and a
    boxplot to compare the distributions of burn probabilities between the two seasons.

    Parameters:
    -----------
    winter_data : numpy.ndarray or list
        A 1D array or list containing burn probabilities for the winter season.
        It will be reshaped into a 2D grid based on `grid_size`.
    summer_data : numpy.ndarray or list
        A 1D array or list containing burn probabilities for the summer season.
        It will be reshaped into a 2D grid based on `grid_size`.
    grid_size : tuple of int, optional
        The dimensions (rows, columns) of the grid used for reshaping the input data.
        Default is (50, 50).

    Outputs:
    --------
    - A figure with two subplots displaying heatmaps for winter and summer data.
    - A separate figure displaying a boxplot comparing burn probabilities for
      winter and summer.
    """
    # Reshape data
    winter_grid = np.array(winter_data).reshape(grid_size)
    summer_grid = np.array(summer_data).reshape(grid_size)

    # 1. Heatmaps
    plot_single_heatmap(winter_grid, 'hot', "Winter Season Burn Probabilities", "Column Index", "Row Index",
                        "Burn Probability")
    plot_single_heatmap(summer_grid, 'hot', "Summer Season Burn Probabilities", "Column Index", "Row Index",
                        "Burn Probability")

    # 2. Boxplot
    winter_data_flat = np.array(winter_data).flatten()
    summer_data_flat = np.array(summer_data).flatten()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.boxplot([winter_data_flat, summer_data_flat], labels=["Winter", "Summer"], showfliers=False)
    ax.set_title("Burn Probability Distribution")
    ax.set_ylabel("Burn Probability")
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Optional: Add a grid to the boxplot
    plt.tight_layout()
    plt.show()
