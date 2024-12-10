import matplotlib.pyplot as plt
from simulate import simulate_fire
import numpy as np
import pandas as pd
from hypothesis1_sim import clear_and_set_fire


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
        burn_probabilities, simulation_results = simulate_fire(grid_with_fire, tree_types, wind_speed, wind_direction, 1)



        # Add wind speed and direction to results
        simulation_results["wind_speed"] = wind_speed
        simulation_results["wind_direction"] = wind_direction

        # Append results to the list
        all_results.append(simulation_results)

    # Combine all results into a single DataFrame
    combined_results = pd.concat(all_results, ignore_index=True)
    return combined_results , burn_probabilities


if __name__ == "__main__":
    import pandas as pd

    # 載入固定地圖和樹種類型
    grid = np.loadtxt("data/data_grid.txt", dtype=int)
    tree_types = np.genfromtxt("data/data_tree_types.txt", dtype=str)
    tree_types[tree_types == "None"] = None

    # 設定要比較的風速和風向
    wind_speeds = [0]  # 三種風速
    wind_direction = "N"  # 北風

    # 執行模擬
    combined_results, burn_probabilities = compare_wind_speeds(grid, tree_types, wind_speeds, wind_direction)

    output_file = "data/wind_burn_probabilities.txt"
    with open(output_file, "w") as file:
        rows, cols = burn_probabilities.shape
        for r in range(rows):
            row_data = " ".join(f"{burn_probabilities[r, c]:.4f}" for c in range(cols))
            file.write(row_data + "\n")

    file_path = 'data/wind_burn_probabilities.txt'  # Replace with your file path
    data = np.loadtxt(file_path)

    # 匯出結果為 CSV
    combined_results.to_csv("wind_speed_comparison_results_0.csv", index=False)
    print("Simulation results saved to 'wind_speed_comparison_results_0.csv'")
