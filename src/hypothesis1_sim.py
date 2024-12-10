from functions import clear_and_set_fire
from functions import find_closest_location
from functions import simulate_multiple_starts
from functions import compare_bush_non_bush
from simulate import simulate_fire
import numpy as np
import pandas as pd

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
    combined_results.to_csv("hypothesis1_df_test.csv", index=False)
