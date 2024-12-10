import numpy as np
from simulate import  simulate_fire
from functions import  plot_fire_and_water_influence, describe_data, plot_heatmap_and_boxplot
from functions import clear_and_set_fire
from functions import find_closest_location
from functions import simulate_multiple_starts
from functions import compare_bush_non_bush
from functions import compare_wind_speeds
from seeds import initialize_grid

# 主程式
if __name__ == "__main__":
    rows, cols = 50,50  # 網格尺寸
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


    ## hypothesis 2 simulation
    # simulate fire

    burn_probabilities, results_df = simulate_fire(grid, tree_types, 10, 'E', 1, True,'winter')


    output_file = "data/burn_probabilities.txt"
    with open(output_file, "w") as file:
        rows, cols = burn_probabilities.shape
        for r in range(rows):
            row_data = " ".join(f"{burn_probabilities[r, c]:.4f}" for c in range(cols))
            file.write(row_data + "\n")

    file_path = 'data/burn_probabilities.txt'  # Replace with your file path
    data = np.loadtxt(file_path)



    # Reshape into a 50x50 matrix
    burn_probabilities = data[:2500].reshape(50, 50)

    plot_fire_and_water_influence(grid, burn_probabilities)


    ## validation simulation
    file_path = 'data/burn_probabilities_summer.txt'  # Replace with your file path
    data = np.loadtxt(file_path)

    # Ensure there are at least 2500 numbers
    if data.size < 2500:
        raise ValueError("The file must contain at least 2500 numbers to form a 50x50 matrix.")
    print("--------------------")
    # Reshape into a 50x50 matrix
    burn_probabilities_summer = data[:2500].reshape(50, 50)

    file_path = 'data/burn_probabilities_winter.txt'  # Replace with your file path
    data = np.loadtxt(file_path)

    # Ensure there are at least 2500 numbers
    if data.size < 2500:
        raise ValueError("The file must contain at least 2500 numbers to form a 50x50 matrix.")

    # Reshape into a 50x50 matrix
    burn_probabilities_winter = data[:2500].reshape(50, 50)
    print("---------------------")
    describe_data(burn_probabilities_winter, 'winter')
    describe_data(burn_probabilities_summer, 'summer')

    # 2. Plot Heatmaps and Boxplot
    plot_heatmap_and_boxplot(burn_probabilities_winter, burn_probabilities_summer)

    ## end










