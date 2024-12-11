import numpy as np
from simulate import simulate_fire
from functions import compare_bush_non_bush, plot_fire_and_water_influence, compare_wind_speeds, describe_data, \
    plot_heatmap_and_boxplot
from seeds import initialize_grid

"""

597PR  Final Project - Monte Carlo Simulation of Wildfire Propagation in Forested Areas

######### Contribution ##########
# Name: Chia-Yu Wang
# 1) Complete the grid initialization function and the main fire simulation function.
# 2) Implement the fire plotting function to visualize the results of each hour during the simulation.
# 3) Implement the function to calculate temperature and humidity.
# 4) Design and implement the simulation for hypothesis 2: The impact of humidity on the likelihood of wildfire spread in areas surrounding bodies of water.
# 5) Design and implement the simulation for validation 1: The impact of seasons (humidity & temperature) on wildfire spread.

# Name: Guan-Hong Lin
# 1) Designed and implemented the cooldowns mechanism to optimize the burn rate in wildfire simulations, ensuring alignment with dynamic environmental conditions.
# 2) Integrated wind direction and wind speed parameters into the simulation, enhancing its accuracy in modeling wildfire spread under diverse conditions.
# 3) Performed extensive research to align simulation parameters with real-world wildfire scenarios, ensuring reliability and scientific validity.
# 4) Designed and implemented a simulation for hypothesis 1: Burned areas increase by approximately 50% when ignition originates from bushland compared to forested areas dominated by willow, pine, and oak trees.
# 5) Designed and implemented a simulation for hypothesis 3: Analyze the relationship between wind speed and wildfire spread, demonstrating that higher wind speeds accelerate spread and reduce burn duration for a given area.
"""

# Main code execution starts here
if __name__ == "__main__":
    rows, cols = 50, 50  # Define the size of the grid (50x50)

    # Step 1: Generate a grid map and tree types
    # The grid represents the area of simulation, and tree_types indicate the type of vegetation in each cell.
    grid, tree_types = initialize_grid(rows, cols, 0.05)  # 5% initialization density for trees

    # Save the generated grid to a file for future use
    with open("data/data_grid.txt", "w") as file:
        for row in grid:
            file.write(" ".join(map(str, row)) + "\n")

    # Save the tree types grid to a file for future use
    with open("data/data_tree_types.txt", "w") as file:
        for row in tree_types:
            file.write(" ".join(map(lambda x: str(x) if x is not None else "None", row)) + "\n")

    # Step 2: Load the saved grid map from files
    # Load the main grid data
    with open('data/data_grid.txt', 'r') as file:
        data = file.readlines()
    grid = np.array([list(map(int, line.split())) for line in data])

    # Load the tree types data
    with open('data/data_tree_types.txt', 'r') as file:
        data = file.readlines()
    tree_types = np.array([line.split() for line in data])

    # Replace 'None' strings with actual None objects (or np.nan for numerical operations)
    tree_types = np.where(tree_types == 'None', None, tree_types)

    # Hypothesis 1: Compare fire simulation results for bush and non-bush tree types
    combined_results_01 = compare_bush_non_bush(grid, tree_types, wind_speed=0, wind_direction="W")

    # Display the results of Hypothesis 1
    print("hypothesis 1 result", combined_results_01, sep=":")

    # Save Hypothesis 1 results to a CSV file for detailed analysis
    combined_results_01.to_csv("data/hypothesis1_df_test.csv", index=False)
    print('Hypothesis 1 simulation complete')

    # Hypothesis 2: Simulate fire spread under specific conditions
    burn_probabilities_02, results_df = simulate_fire(grid, tree_types, 10, 'E', 1, True, 'winter')

    # Save burn probabilities to a file for further analysis
    output_file_02 = "data/burn_probabilities.txt"
    with open(output_file_02, "w") as file:
        rows, cols = burn_probabilities_02.shape
        for r in range(rows):
            row_data = " ".join(f"{burn_probabilities_02[r, c]:.4f}" for c in range(cols))
            file.write(row_data + "\n")

    # Load the saved burn probabilities data
    file_path_02 = 'data/burn_probabilities.txt'
    data_02 = np.loadtxt(file_path_02)

    # Reshape the burn probabilities into a 50x50 matrix
    burn_probabilities_02 = data_02[:2500].reshape(50, 50)

    # Visualize the influence of fire and water on burn probabilities
    plot_fire_and_water_influence(grid, burn_probabilities_02)
    print('Hypothesis 2 simulation complete')

    # Hypothesis 3: Investigate the effect of wind speed and direction on fire spread
    wind_speeds_03 = [10]  # Define wind speeds for the simulation
    wind_direction_03 = "N"  # Define wind direction for the simulation

    # Conduct the fire spread simulation under varying wind conditions
    combined_results_03, burn_probabilities_03 = compare_wind_speeds(grid, tree_types, wind_speeds_03,
                                                                     wind_direction_03)

    # Save the results of wind-speed-influenced burn probabilities
    output_file_03 = "data/wind_burn_probabilities.txt"
    with open(output_file_03, "w") as file:
        rows, cols = burn_probabilities_03.shape
        for r in range(rows):
            row_data = " ".join(f"{burn_probabilities_03[r, c]:.4f}" for c in range(cols))
            file.write(row_data + "\n")

    # Load and reshape the wind-speed-influenced burn probabilities
    file_path_03 = 'data/wind_burn_probabilities.txt'
    data_03 = np.loadtxt(file_path_03)
    burn_probabilities_03 = data_03[:2500].reshape(50, 50)

    # Save the wind speed comparison results for further analysis
    combined_results_03.to_csv("data/wind_speed_comparison_results_test.csv", index=False)
    print('Hypothesis 3 simulation complete')

    # Validation Simulation: Compare fire spread probabilities in different seasons
    # Load and reshape the burn probabilities for summer
    file_path_summer = 'data/burn_probabilities_summer.txt'
    data_summer = np.loadtxt(file_path_summer)
    burn_probabilities_summer = data_summer[:2500].reshape(50, 50)

    # Load and reshape the burn probabilities for winter
    file_path_winter = 'data/burn_probabilities_winter.txt'
    data_winter = np.loadtxt(file_path_winter)
    burn_probabilities_winter = data_winter[:2500].reshape(50, 50)

    # Describe the data for each season to analyze statistical differences
    describe_data(burn_probabilities_winter, 'winter')
    describe_data(burn_probabilities_summer, 'summer')

    # Plot heatmaps and boxplots to visually compare fire spread between seasons
    plot_heatmap_and_boxplot(burn_probabilities_winter, burn_probabilities_summer)
    print('Validation simulation complete')

# End of script
