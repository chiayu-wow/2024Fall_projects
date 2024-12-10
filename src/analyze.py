import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt


def plot_fire_and_water_influence(grid, burn_probabilities):
    # Water cells (grid == 3)
    water_cells = (grid == 3)

    # Calculate the distance to the nearest water
    distances_to_water = distance_transform_edt(~water_cells)

    # Set the maximum influence distance for water and adjust burn probabilities
    max_influence_distance = 5
    influence_factor = np.clip(1 - (distances_to_water / max_influence_distance), 0, 1)

    # Adjust burn probabilities based on water proximity
    adjusted_burn_probabilities = burn_probabilities * (1 - 0.5 * influence_factor)

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
    ax.contour(water_cells, colors='blue', linewidths=0.5, linestyles='dashed', label="Water Bodies")
    ax.legend(["Water Bodies"])

    # Plot 2: Distance to Water Heatmap
    ax = axes[1]
    img2 = ax.imshow(distances_to_water, cmap="cool", interpolation="nearest")
    ax.set_title("Distance to Water Heatmap")
    ax.set_xlabel("Column Index")
    ax.set_ylabel("Row Index")
    cbar2 = plt.colorbar(img2, ax=ax)
    cbar2.set_label("Distance to Water (Cells)")
    ax.contour(water_cells, colors='blue', linewidths=0.5, linestyles='dashed', label="Water Bodies")
    ax.legend(["Water Bodies"])

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
    Print summary statistics of burn probabilities for the given season.
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
    Plots a heatmap of burn probabilities for both winter and summer seasons and
    a boxplot to compare the distribution of burn probabilities for both seasons.
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
