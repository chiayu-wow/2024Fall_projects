import numpy as np

def initialize_grid(rows, cols, water_body_ratio=0.2, fire_location=(25, 25), num_water_bodies=2):
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.15, 0.85])  # 15% 空地，85% 樹木
    grid[fire_location] = 2  # 火災初始點設為 (10, 10)

    # 計算總水體格子數
    total_water_cells = int(rows * cols * water_body_ratio)
    water_cells_per_body = total_water_cells // num_water_bodies

    # 紀錄所有水體格子
    all_water_cells = set()

    # 為每個水體聚集區域生成格子
    for _ in range(num_water_bodies):
        water_center = (np.random.randint(0, rows), np.random.randint(0, cols))
        water_cells = set()
        water_cells.add(water_center)

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

    # 更新水體到 grid
    for i, j in all_water_cells:
        grid[i, j] = 3  # 設置水體為 3

    # 樹木類型
    tree_types = np.empty_like(grid, dtype=object)
    tree_types[grid == 1] = np.random.choice(["pine", "oak", "palm", "bush"], size=np.sum(grid == 1))

    return grid, tree_types
