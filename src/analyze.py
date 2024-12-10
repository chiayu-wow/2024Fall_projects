import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt

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
        3. Generates three visualizations:
           - Heatmap of initial burn probabilities.
           - Heatmap of distances to water.
           - Boxplot comparing burn probabilities of cells close to water (distance ≤ 5) and far from water (distance > 5).

        Visualizations:
        ---------------
        - **Burn Probabilities Heatmap**:
            Displays the initial burn probabilities for all cells using a "hot" color map.
        - **Distance to Water Heatmap**:
            Illustrates the calculated distances to the nearest water cell for each grid cell using a "cool" color map.
        - **Boxplot of Burn Probabilities**:
            Compares the distributions of burn probabilities for cells near and far from water.

        Console Output:
        ---------------
        Prints summary statistics for burn probabilities of:
        - Cells close to water (distance ≤ 5).
        - Cells far from water (distance > 5).
        Statistics include:
        - Mean
        - Median
        - Standard deviation

        Returns: None
    """

    water_cells = (grid == 3)

    # Calculate the distance to the nearest water
    distances_to_water = distance_transform_edt(~water_cells)

    # Set the maximum influence distance for water and adjust burn probabilities
    max_influence_distance = 5
    influence_factor = np.clip(1 - (distances_to_water / max_influence_distance), 0, 1)

    # Create visualizations
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Plot 1: Burn Probabilities Heatmap
    ax = axes[0]
    img1 = ax.imshow(burn_probabilities, cmap="hot", interpolation="nearest")
    ax.set_title("Burn Probabilities Heatmap")
    ax.set_xlabel("Column Index")
    ax.set_ylabel("Row Index")
    cbar1 = plt.colorbar(img1, ax=ax)
    cbar1.set_label("Burn Probability")
    # Contour plot of water cells
    ax.legend(['Water Bodies'], loc='best')

    # Plot 2: Distance to Water Heatmap
    ax = axes[1]
    img2 = ax.imshow(distances_to_water, cmap="cool", interpolation="nearest")
    ax.set_title("Distance to Water Heatmap")
    ax.set_xlabel("Column Index")
    ax.set_ylabel("Row Index")
    cbar2 = plt.colorbar(img2, ax=ax)
    cbar2.set_label("Distance to Water (Cells)")
    # Contour plot of water cells
    ax.legend(['Water Bodies'], loc='best')

    # Plot 3: Boxplot and Statistical Analysis
    ax = axes[2]

    # Extract burn probabilities for cells near water (distance <= 5 cells) and far from water (distance > 5)
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

    print("Statistics for cells close to water (distance <= 5 cells):")
    print(f"Mean: {stats_close['mean']:.4f}, Median: {stats_close['median']:.4f}, Std: {stats_close['std']:.4f}")

    print("\nStatistics for cells far from water (distance > 5 cells):")
    print(f"Mean: {stats_far['mean']:.4f}, Median: {stats_far['median']:.4f}, Std: {stats_far['std']:.4f}")

    plt.tight_layout()
    plt.show()

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

        Functionality:
        --------------
        - Creates two heatmaps:
            - One for winter burn probabilities.
            - One for summer burn probabilities.
        - Displays the heatmaps with colorbars and appropriate labels.
        - Creates a boxplot to compare the distributions of burn probabilities
          between winter and summer seasons.

        Outputs:
        --------
        - A figure with two subplots displaying heatmaps for winter and summer data.
        - A separate figure displaying a boxplot comparing burn probabilities for
          winter and summer.
    """
    # 1. Heatmap of Burn Probabilities
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Winter Heatmap
    ax = axes[0]
    ax.imshow(winter_data.reshape(grid_size), cmap='hot', interpolation='nearest')
    ax.set_title("Winter Season Burn Probabilities")
    ax.set_xlabel("Column Index")
    ax.set_ylabel("Row Index")
    cbar = plt.colorbar(ax.imshow(winter_data.reshape(grid_size), cmap='hot', interpolation='nearest'), ax=ax)
    cbar.set_label("Burn Probability")

    # Summer Heatmap
    ax = axes[1]
    ax.imshow(summer_data.reshape(grid_size), cmap='hot', interpolation='nearest')
    ax.set_title("Summer Season Burn Probabilities")
    ax.set_xlabel("Column Index")
    ax.set_ylabel("Row Index")
    cbar = plt.colorbar(ax.imshow(summer_data.reshape(grid_size), cmap='hot', interpolation='nearest'), ax=ax)
    cbar.set_label("Burn Probability")

    plt.tight_layout()
    plt.show()

    # 2. Boxplot of Burn Probabilities
    # Reshaping the 1D data into 2D to pass into boxplot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.boxplot([winter_data.flatten(), summer_data.flatten()], labels=["Winter", "Summer"])
    ax.set_title("Burn Probability Distribution")
    ax.set_ylabel("Burn Probability")
    plt.show()
