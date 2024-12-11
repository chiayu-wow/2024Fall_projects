import numpy as np

def initialize_grid(rows, cols, water_body_ratio=0.1, fire_location=(25, 25), num_water_bodies=10, bush_ratio=0.05,
                    nums_of_busharea=4):
    """
        Initializes a grid representing a forest ecosystem with various elements like trees, bushes,
        water bodies, and a fire starting point. The grid is populated based on the specified parameters.

        Parameters:
        -----------
        rows : int
            The number of rows in the grid.
        cols : int
            The number of columns in the grid.
        water_body_ratio : float, optional
            The ratio of grid cells to be designated as water bodies. Default is 0.1 (10%).
        fire_location : tuple of int, optional
            The (row, column) coordinates where the fire starts. Default is (25, 25).
        num_water_bodies : int, optional
            The number of distinct water bodies to create. Default is 10.
        bush_ratio : float, optional
            The proportion of tree cells that will be converted into bushes. Default is 0.05 (5% of trees).
        nums_of_busharea : int, optional
            The number of separate bush areas to create. Default is 4.

        Returns:
        --------
        grid : numpy.ndarray
            A 2D grid representing the forest with the following cell values:
            - 0: Empty cell
            - 1: Tree
            - 2: Fire start location
            - 3: Water body
            - 5: Bush
        tree_types : numpy.ndarray
            A 2D array of the same shape as `grid`, containing the types of trees or bushes for cells with trees:
            - "pine", "oak", or "willow" for tree cells
            - "bush" for bush cells
            - None for non-tree/non-bush cells

        Examples:
        ---------
        >>> grid, tree_types = initialize_grid(10, 10, water_body_ratio=0.2, fire_location=(5, 5), bush_ratio=0.1)
        >>> grid.shape
        (10, 10)
        >>> grid[5, 5] == 2
        True
        >>> np.sum(grid == 3) <= 10 * 10 * 0.2  # Ensure water bodies match ratio
        True
        >>> np.sum(grid == 5) <= np.sum(grid == 1) * 0.1  # Ensure bushes are no more than 10% of trees
        True
        >>> tree_types.shape == grid.shape
        True
    """
    # Initialize grid: 0 = empty, 1 = tree
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.15, 0.85])  # 15% empty, 85% plants
    grid[fire_location] = 2  # Fire start location

    # Calculate total water cells and assign water areas
    total_water_cells = int(rows * cols * water_body_ratio)
    water_cells_per_body = total_water_cells // num_water_bodies
    all_water_cells = set()

    for _ in range(num_water_bodies):
        water_center = (np.random.randint(0, rows), np.random.randint(0, cols))
        water_cells = {water_center}

        while len(water_cells) < water_cells_per_body:
            current_cell = list(water_cells)[np.random.randint(0, len(water_cells))]
            neighbors = [
                (current_cell[0] + dx, current_cell[1] + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= current_cell[0] + dx < rows and 0 <= current_cell[1] + dy < cols
                   and (current_cell[0] + dx, current_cell[1] + dy) not in all_water_cells
            ]
            if neighbors:
                new_cell = neighbors[np.random.randint(0, len(neighbors))]
                water_cells.add(new_cell)

        all_water_cells.update(water_cells)

    for i, j in all_water_cells:
        grid[i, j] = 3  # Mark water cells

    # Assign bushes to specific areas
    total_trees = np.sum(grid == 1)
    total_bushes = int(total_trees * bush_ratio)
    bushes_per_area = total_bushes // nums_of_busharea
    all_bush_cells = set()

    for _ in range(nums_of_busharea):
        bush_center = (np.random.randint(0, rows), np.random.randint(0, cols))
        while grid[bush_center] != 1:  # Ensure bush center is a tree
            bush_center = (np.random.randint(0, rows), np.random.randint(0, cols))

        bush_cells = {bush_center}

        while len(bush_cells) < bushes_per_area:
            current_cell = list(bush_cells)[np.random.randint(0, len(bush_cells))]
            neighbors = [
                (current_cell[0] + dx, current_cell[1] + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= current_cell[0] + dx < rows and 0 <= current_cell[1] + dy < cols
                   and (current_cell[0] + dx, current_cell[1] + dy) not in all_bush_cells
                   and grid[current_cell[0] + dx, current_cell[1] + dy] == 1  # Only trees become bushes
            ]
            if neighbors:
                new_cell = neighbors[np.random.randint(0, len(neighbors))]
                bush_cells.add(new_cell)

        all_bush_cells.update(bush_cells)

    for i, j in all_bush_cells:
        grid[i, j] = 5  # Mark bush cells

    # Tree types: assign types to trees and bushes
    tree_types = np.empty_like(grid, dtype=object)
    tree_types[grid == 1] = np.random.choice(["pine", "oak", "willow"], size=np.sum(grid == 1))
    tree_types[grid == 5] = "bush"  # Assign bushes explicitly

    return grid, tree_types
