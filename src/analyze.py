import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt
from plot import  create_heatmap, plot_single_heatmap

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
        distances_to_water, "cool", "Distance to Water Heatmap", "Column Index", "Row Index", "Distance to Water (Cells)"
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
    plot_single_heatmap(winter_grid, 'hot', "Winter Season Burn Probabilities", "Column Index", "Row Index", "Burn Probability")
    plot_single_heatmap(summer_grid, 'hot', "Summer Season Burn Probabilities", "Column Index", "Row Index", "Burn Probability")

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
