# Define tree flammability mapping
tree_flammability: dict[str, float] = {
    "pine": 0.8,  # Pine tree with high flammability
    "oak": 0.7,  # Oak tree with medium flammability
    "willow": 0.5,  # Willow tree with low flammability
    "bush": 0.95,  # Bush with very high flammability
    "none": 0.0  # Empty or unplanted land with no flammability
}

# Define tree colors mapping
tree_colors: dict[str, str] = {
    "pine": "darkgreen",  # Pine tree - dark green
    "oak": "green",  # Oak tree - green
    "willow": "seagreen",  # Willow tree - sea green
    "none": "brown"  # Empty or unplanted land - brown
}

# Define tree burn rates mapping
tree_burn_rates: dict[str, float] = {
    "bush": 46 / 46,  # Bush burns the fastest, fully burning in one step
    "pine": 20 / 46,  # Pine tree burns moderately fast
    "oak": 15 / 46,  # Oak tree burns slower than pine
    "willow": 10 / 46,  # Willow tree burns the slowest among trees
    "none": 0.0  # Empty or unplanted land does not burn
}
