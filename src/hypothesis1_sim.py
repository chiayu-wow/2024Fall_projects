import matplotlib.pyplot as plt
from simulate import simulate_fire
import numpy as np
import pandas as pd


def clear_and_set_fire(grid, start_point):
    """
    Clears all fire points and sets a new fire point.

    :param grid: numpy array, simulation grid
    :param start_point: tuple, fire point coordinates (row, col)
    :return: numpy array, the updated grid with the new fire point
    """
    grid_copy = grid.copy()
    grid_copy[grid_copy == 2] = 0  # Clear all potential fire sources
    grid_copy[start_point] = 2  # Set the unique fire point
    return grid_copy


def find_closest_location(grid, tree_types, target_type, center=(25, 25)):
    """
    Finds the location of the specified type that is closest to the center.

    :param grid: numpy array, simulation grid
    :param tree_types: numpy array, tree type grid
    :param target_type: str, target type ('bush' or 'non_bush')
    :param center: tuple, center coordinates (row, col)
    :return: tuple, the closest location
    """
    if target_type == "bush":
        # Find all Bush locations
        locations = list(zip(*np.where(grid == 5)))
    elif target_type == "non_bush":
        # Find all Non-Bush locations
        locations = list(zip(*np.where((grid == 1) & (tree_types != "bush"))))
    else:
        raise ValueError("Invalid target_type. Use 'bush' or 'non_bush'.")

    # Calculate the Euclidean distance of each location to the center
    distances = [((loc[0] - center[0]) ** 2 + (loc[1] - center[1]) ** 2, loc) for loc in locations]

    # Sort by distance
    distances.sort(key=lambda x: x[0])

    # Return the closest location
    return distances[0][1] if distances else None


def simulate_multiple_starts(grid, tree_types, start_locations, wind_speed=0, wind_direction="W"):
    """
    Simulates multiple fire starting points, recording burned area and time for each.

    :param grid: numpy array, simulation grid
    :param tree_types: numpy array, tree type grid
    :param start_locations: list of tuples, list of fire point coordinates
    :param wind_speed: float, wind speed
    :param wind_direction: str, wind direction (N, E, S, W)
    :return: pandas DataFrame, combined results for all simulations
    """
    all_results = []  # List to store DataFrame for each simulation

    for start_point in start_locations:
        # Set a new fire point
        grid_with_fire = clear_and_set_fire(grid, start_point)

        # Simulate
        _, simulation_results = simulate_fire(grid_with_fire, tree_types, wind_speed, wind_direction, simulations=50)

        # Append the DataFrame directly to the list
        all_results.append(simulation_results)

        # Simulate only once, then exit
        break  # Simulate for only one fire point

    # Combine all results into a single DataFrame
    combined_results = pd.concat(all_results, ignore_index=True)
    return combined_results


def compare_bush_non_bush(grid, tree_types, wind_speed=0, wind_direction="W"):
    """
    Compares simulation results for fire points starting in bush and non-bush areas.

    :param grid: numpy array, simulation grid
    :param tree_types: numpy array, tree type grid
    :param wind_speed: float, wind speed
    :param wind_direction: str, wind direction (N, E, S, W)
    :return: pandas DataFrame, combined results for Bush and Non-Bush simulations
    """
    # Define the center point
    center_point = (25, 25)

    # Find the closest Bush and Non-Bush fire points to the center
    closest_bush = find_closest_location(grid, tree_types, target_type="bush", center=center_point)
    closest_non_bush = find_closest_location(grid, tree_types, target_type="non_bush", center=center_point)

    # Initialize result variables
    results_bush = pd.DataFrame()
    results_non_bush = pd.DataFrame()

    # Bush simulation
    if closest_bush:
        print(f"Simulating fire point (Bush): {closest_bush}")
        results_bush = simulate_multiple_starts(grid, tree_types, [closest_bush], wind_speed=wind_speed,
                                                wind_direction=wind_direction)
        results_bush["category"] = "fire_at_bush"  # Add category column
    else:
        print("No valid Bush fire point found.")

    # Non-Bush simulation
    if closest_non_bush:
        print(f"Simulating fire point (Non-Bush): {closest_non_bush}")
        results_non_bush = simulate_multiple_starts(grid, tree_types, [closest_non_bush], wind_speed=wind_speed,
                                                    wind_direction=wind_direction)
        results_non_bush["category"] = "fire_at_non_bush"  # Add category column
    else:
        print("No valid Non-Bush fire point found.")

    # Combine the results into a single DataFrame
    combined_results = pd.concat([results_bush, results_non_bush], ignore_index=True)

    return combined_results


if __name__ == "__main__":
    # Load fixed grid and tree types
    grid = np.loadtxt("data_grid.txt", dtype=int)
    tree_types = np.genfromtxt("data_tree_types.txt", dtype=str)
    tree_types[tree_types == "None"] = None

    # Compare simulation results for Bush and Non-Bush
    combined_results = compare_bush_non_bush(grid, tree_types, wind_speed=0, wind_direction="W")

    # Display the combined results
    print(combined_results)

    # Save the results to a CSV file for further analysis
    combined_results.to_csv("hypothesis1_df.csv", index=False)
