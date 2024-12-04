import numpy as np

def initialize_grid(rows, cols, water_body_ratio=0.2, fire_location=(10, 10), num_water_bodies = 2):
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
    tree_types[grid == 1] = np.random.choice(["pine", "oak", "palm"], size=np.sum(grid == 1))

    temperatures = np.full_like(grid, 25.0, dtype=float)  # 初始化所有格子溫度為 25°C
    humidities = np.zeros_like(grid, dtype=float)  # 初始化所有格子的濕度為 0

    # 設定火災格子的高溫影響
    temperatures[grid == 2] = 100  # 火災格子的溫度為 100°C

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 3:  # 水體
                humidities[i, j] = 0.8  # 改為水體的濕度設為 0.8
                for x in range(rows):
                    for y in range(cols):
                        if grid[x, y] == 3:
                            continue  # 跳過其他水體格子
                        distance = abs(i - x) + abs(j - y)  # 計算曼哈頓距離
                        # 只影響距離水體 4 格內的格子，並且濕度隨距離遞減
                        if distance <= 4 and grid[x, y] != 2:  # 不對火災格子進行濕度增加
                            humidities[x, y] += 0.8 / (distance + 2)  # 隨著距離衰減濕度

    # 設定火災影響範圍內的格子溫度上升
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 2:  # 火災格子
                for x in range(max(0, i - 1), min(rows, i + 2)):
                    for y in range(max(0, j - 1), min(cols, j + 2)):
                        temperatures[x, y] = min(100, temperatures[x, y] + 5)  # 火災範圍內溫度上升

    return grid, tree_types, temperatures, humidities
