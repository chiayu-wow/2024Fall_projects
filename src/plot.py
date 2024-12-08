import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb  # Import to_rgb from matplotlib.colors
import numpy as np
from data import  tree_colors

def plot_fire(grid, tree_types, step):
    # Initialize grid for colored visualization
    rows, cols = grid.shape
    grid_colored = np.zeros((rows, cols, 3), dtype=int)  # RGB color grid

    # Map grid values to corresponding colors
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:  # Tree cell
                tree_type = tree_types[r, c]  # Get tree type at this position
                tree_color = tree_colors.get(tree_type, "brown")  # Get the tree color, default to brown
                grid_colored[r, c] = np.array(to_rgb(tree_color)) * 255  # Convert to RGB values
            elif grid[r, c] == 3:  # Water cell
                grid_colored[r, c] = np.array(to_rgb("blue")) * 255  # Blue for water
            elif grid[r, c] == 2:  # Fire cell
                grid_colored[r, c] = np.array(to_rgb("red")) * 255  # Red for fire
            elif grid[r, c] == 4:  # Burnt cell
                grid_colored[r, c] = np.array(to_rgb("black")) * 255  # Black for burnt area
            else:  # Empty land or any other type
                grid_colored[r, c] = np.array(to_rgb("brown")) * 255  # Brown for empty land

    # Plot the grid using the colors
    plt.imshow(grid_colored, interpolation='nearest')
    plt.colorbar(ticks=[0, 1, 2, 3, 4], label="Cell Type")
    plt.title(f"Fire Spread Simulation - Step {step}")
    plt.pause(0.1)  # Pause to update the plot
    plt.clf()  # Clear the figure for the next plot
