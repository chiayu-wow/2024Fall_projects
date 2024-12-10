from functions import compare_wind_speeds
from simulate import simulate_fire
import numpy as np
from hypothesis1_sim import clear_and_set_fire

if __name__ == "__main__":
    import pandas as pd

    # 載入固定地圖和樹種類型
    grid = np.loadtxt("data/data_grid.txt", dtype=int)
    tree_types = np.genfromtxt("data/data_tree_types.txt", dtype=str)
    tree_types[tree_types == "None"] = None

    # 設定要比較的風速和風向
    wind_speeds = [0]  # 三種風速
    wind_direction = "N"  # 北風

    # 執行模擬
    combined_results, burn_probabilities = compare_wind_speeds(grid, tree_types, wind_speeds, wind_direction)

    output_file = "data/wind_burn_probabilities.txt"
    with open(output_file, "w") as file:
        rows, cols = burn_probabilities.shape
        for r in range(rows):
            row_data = " ".join(f"{burn_probabilities[r, c]:.4f}" for c in range(cols))
            file.write(row_data + "\n")

    file_path = 'data/wind_burn_probabilities.txt'  # Replace with your file path
    data = np.loadtxt(file_path)

    # 匯出結果為 CSV
    combined_results.to_csv("wind_speed_comparison_results_test.csv", index=False)
    print("Simulation results saved to 'wind_speed_comparison_results_0.csv'")
