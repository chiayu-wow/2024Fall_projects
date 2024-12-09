tree_flammability = {
    "pine": 0.85,  # 松樹，高可燃性
    "oak": 0.55,  # 橡樹，低等可燃性
    "willow": 0.7,  # 柳樹，中可燃性
    "bush": 0.95,
    None: 0.0
}

# Define tree colors mapping
tree_colors = {
    "pine": "darkgreen",  # 松樹 (Pine) - Green
    "oak": "green",  # 橡樹 (Oak) - Dark Green
    "willow": "seagreen",  # 柳樹 (willow) - Yellow Green
    None: "brown"  # Empty or unplanted land - Brown
}

# 燃燒速率（單位：步驟數，每步擴散多少單位）
tree_burn_rates = {
    "bush": 46 / 46,  # 灌木叢：每小時 46 chain，約 1 格/hour 燃燒最快，每一步可覆蓋整個網格單位
    "pine": 20 / 46,  # 松樹
    "oak": 15 / 46,  # 橡樹
    "willow": 10 / 46,  # 柳樹
    None: 0.0
}
