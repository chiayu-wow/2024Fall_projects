tree_flammability = {
    "pine": 0.8,  # 松樹，高可燃性
    "oak": 0.4,  # 橡樹，低等可燃性
    "palm": 0.6,  # 棕櫚樹，中可燃性
    "bush": 0.95,
    None: 0.0
}

# Define tree colors mapping
tree_colors = {
    "pine": "green",  # 松樹 (Pine) - Green
    "oak": "darkgreen",  # 橡樹 (Oak) - Dark Green
    "palm": "yellowgreen",  # 棕櫚樹 (Palm) - Yellow Green
    None: "brown",  # Empty or unplanted land - Brown
    "bush": "lightgreen"  # Bush - Light Green
}

# 燃燒速率（單位：步驟數，每步擴散多少單位）
tree_burn_rates = {
    "bush": 46 / 46,  # 灌木叢：每小時 46 chain，約 1 格/hour 燃燒最快，每一步可覆蓋整個網格單位
    "pine": 15 / 46,  # 松樹：每小時 15 chain，約 0.33 格/hour 燃燒速度中等，因樹脂高度易燃，大約需要 3 步覆蓋一個網格。
    "oak": 5 / 46,  # 橡樹：每小時 5 chain，約 0.11 格/hour 燃燒速度最慢，因水分含量高且木質不易燃，大約需要 9 步覆蓋一個網格
    "palm": 25 / 46,  # 棕櫚：每小時 25 chain，約 0.54 格/hour 燃燒速度比松樹快但比灌木慢，因為纖維和油脂容易燃燒，大約 2 步覆蓋一個網
    None: 0.0
}
