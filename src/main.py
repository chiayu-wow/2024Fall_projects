import numpy as np
from simulate import simulate_fire
from functions import compare_bush_non_bush, plot_fire_and_water_influence, compare_wind_speeds, describe_data, \
    plot_heatmap_and_boxplot
from seeds import initialize_grid

# 主程式
if __name__ == "__main__":
    rows, cols = 50, 50  # 網格尺寸
    # generate grip map
    '''
    grid, tree_types = initialize_grid(rows, cols, 0.05)
    
    with open("data/data_grid.txt", "w") as file:
        for row in grid:
            file.write(" ".join(map(str, row)) + "\n")
    
    with open("data/data_tree_types.txt", "w") as file:
        for row in tree_types:
            file.write(" ".join(map(lambda x: str(x) if x is not None else "None", row)) + "\n")

    '''
    # read grip map
    with open('data/data_grid.txt', 'r') as file:
        data = file.readlines()

    grid = np.array([list(map(int, line.split())) for line in data])

    with open('data/data_tree_types.txt', 'r') as file:
        data = file.readlines()

    tree_types = np.array([line.split() for line in data])
    # Replace 'None' strings with `None` objects or np.nan (if needed for numerical operations)
    tree_types = np.where(tree_types == 'None', None, tree_types)

    ## hypothesis 1 simulation ##
    # Compare simulation results for Bush and Non-Bush
    combined_results_01 = compare_bush_non_bush(grid, tree_types, wind_speed=0, wind_direction="W")

    # Display the combined results
    print("hypothesis 1 result", combined_results_01, sep=":")
    # Save the results to a CSV file for further analysis
    combined_results_01.to_csv("data/hypothesis1_df_test.csv", index=False)

    ## hypothesis 2 simulation ##
    # simulate fire

    burn_probabilities_02, results_df = simulate_fire(grid, tree_types, 10, 'E', 1, True, 'winter')

    output_file_02 = "data/burn_probabilities.txt"
    with open(output_file_02, "w") as file:
        rows, cols = burn_probabilities_02.shape
        for r in range(rows):
            row_data = " ".join(f"{burn_probabilities_02[r, c]:.4f}" for c in range(cols))
            file.write(row_data + "\n")

    file_path_02 = 'data/burn_probabilities.txt'  # Replace with your file path
    data_02 = np.loadtxt(file_path_02)

    # Reshape into a 50x50 matrix
    burn_probabilities_02 = data_02[:2500].reshape(50, 50)

    plot_fire_and_water_influence(grid, burn_probabilities_02)

    ## hypothesis 3 simulation ##
    # 設定要比較的風速和風向
    wind_speeds_03 = [0]  # 三種風速
    wind_direction_03 = "N"  # 北風

    # 執行模擬
    combined_results_03, burn_probabilities_03 = compare_wind_speeds(grid, tree_types, wind_speeds_03,
                                                                     wind_direction_03)

    output_file_03 = "data/wind_burn_probabilities.txt"
    with open(output_file_03, "w") as file:
        rows, cols = burn_probabilities_03.shape
        for r in range(rows):
            row_data = " ".join(f"{burn_probabilities_03[r, c]:.4f}" for c in range(cols))
            file.write(row_data + "\n")

    file_path_03 = 'data/wind_burn_probabilities.txt'  # Replace with your file path
    data_03 = np.loadtxt(file_path_03)

    # Reshape into a 50x50 matrix
    burn_probabilities_03 = data_03[:2500].reshape(50, 50)

    # 匯出結果為 CSV
    combined_results_03.to_csv("data/wind_speed_comparison_results_test.csv", index=False)
    print("Simulation results saved to 'wind_speed_comparison_results_test.csv'")

    ## validation simulation ##
    # summer
    file_path_summer = 'data/burn_probabilities_summer.txt'  # Replace with your file path
    data_summer = np.loadtxt(file_path_summer)

    # Reshape into a 50x50 matrix
    burn_probabilities_summer = data_summer[:2500].reshape(50, 50)

    # winter
    file_path_winter = 'data/burn_probabilities_winter.txt'  # Replace with your file path
    data_winter = np.loadtxt(file_path_winter)

    # Reshape into a 50x50 matrix
    burn_probabilities_winter = data_winter[:2500].reshape(50, 50)

    # describe data
    describe_data(burn_probabilities_winter, 'winter')
    describe_data(burn_probabilities_summer, 'summer')

    # 2. Plot Heatmaps and Boxplot
    plot_heatmap_and_boxplot(burn_probabilities_winter, burn_probabilities_summer)

    ## end
