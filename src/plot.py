import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb  # Import to_rgb from matplotlib.colors
import numpy as np
from data import tree_colors


def plot_fire(grid, tree_types, hours):
    """
    Visualize the fire spread simulation with a color-coded grid.

    Parameters:
    -----------
    grid : np.ndarray
        2D array representing the simulation grid, where:
        - 1 represents tree cells.
        - 2 represents fire cells.
        - 3 represents water cells.
        - 4 represents burnt cells.
        - 5 represents areas with reduced fire spread.
        - Any other value represents empty land.
    tree_types : np.ndarray
        2D array representing the type of trees at each grid position.
        Each tree type corresponds to a predefined color in `tree_colors`.
    hours : int
        The number of hours elapsed in the simulation, used in the plot title.

    Returns:
    --------
    None

    Example:
    --------
    >>> grid = np.array([[1, 2, 3], [4, 5, 0]])
    >>> tree_types = np.array([['oak', 'oak', 'oak'], ['oak', 'oak', 'oak']])
    >>> tree_colors = {'oak': 'green'}
    >>> plot_fire(grid, tree_types, 2)  # Visualizes the grid for 2 hours of simulation.
    """
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
            elif grid[r, c] == 5:  # Reduced fire spread area
                grid_colored[r, c] = np.array(to_rgb("mediumseagreen")) * 255  # Medium sea green for reduced spread
            else:  # Empty land or any other type
                grid_colored[r, c] = np.array(to_rgb("brown")) * 255  # Brown for empty land

    # Plot the grid using the colors
    plt.imshow(grid_colored, interpolation='nearest')
    plt.colorbar(ticks=[0, 1, 2, 3, 4], label="Cell Type")
    plt.title(f"{hours} hour(s) of Fire Spread")
    plt.pause(0.1)  # Pause to update the plot
    plt.clf()  # Clear the figure for the next plot


def create_heatmap(ax, data, cmap, title, xlabel, ylabel, colorbar_label):
    """
    Helper function to create a heatmap visualization.

    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes on which to plot the heatmap.
    data : numpy.ndarray
        The data to display in the heatmap.
    cmap : str
        The colormap to use for the heatmap.
    title : str
        The title of the heatmap.
    xlabel : str
        The label for the x-axis.
    ylabel : str
        The label for the y-axis.
    colorbar_label : str
        The label for the colorbar.

    Returns:
    --------
    None

    Example:
    --------
    >>> fig, ax = plt.subplots()
    >>> data = np.array([[1, 2], [3, 4]])
    >>> create_heatmap(ax, data, cmap='viridis', title='Heatmap', xlabel='X-axis', ylabel='Y-axis', colorbar_label='Values')
    """
    # Plot the heatmap using the specified colormap
    img = ax.imshow(data, cmap=cmap, interpolation="nearest")
    ax.set_title(title)  # Set the title of the heatmap
    ax.set_xlabel(xlabel)  # Label the x-axis
    ax.set_ylabel(ylabel)  # Label the y-axis
    cbar = plt.colorbar(img, ax=ax)  # Add a colorbar
    cbar.set_label(colorbar_label)  # Label the colorbar


def plot_single_heatmap(data, cmap, title, xlabel, ylabel, colorbar_label):
    """
    Plot a single heatmap.

    Parameters:
    -----------
    data : numpy.ndarray
        The data to display in the heatmap.
    cmap : str
        The colormap to use for the heatmap.
    title : str
        The title of the heatmap.
    xlabel : str
        The label for the x-axis.
    ylabel : str
        The label for the y-axis.
    colorbar_label : str
        The label for the colorbar.

    Returns:
    --------
    None

    Example:
    --------
    >>> data = np.array([[1, 2, 3], [4, 5, 6]])
    >>> plot_single_heatmap(data, cmap='plasma', title='Example Heatmap', xlabel='X-axis', ylabel='Y-axis', colorbar_label='Value Intensity')
    """
    # Create a new figure and axis for the heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    create_heatmap(ax, data, cmap, title, xlabel, ylabel, colorbar_label)  # Use the helper function
    plt.tight_layout()  # Adjust the layout to prevent overlap
    plt.show()  # Display the heatmap
