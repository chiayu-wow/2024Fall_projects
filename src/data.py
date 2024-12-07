tree_flammability = {
    "pine": 0.8,  # 松樹，高可燃性
    "oak": 0.4,   # 橡樹，低等可燃性
    "palm": 0.6,  # 棕櫚樹，中可燃性
    "bush" : 0.95,
    None : 0.0
}

tree_colors = {
    "pine": "green",  # 松樹為綠色
    "oak": "darkgreen",  # 橡樹為深綠色
    "palm": "yellowgreen"  # 棕櫚樹為黃綠色
}

import numpy as np

grid = np.array([
    [1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 3, 3, 1],
    [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 3, 3, 0, 1]
])

tree_types = np.array([['pine', None, 'pine', 'bush', 'bush', 'oak', 'bush', None, 'pine', None, 'palm',
  'pine', 'palm', 'oak', 'oak', 'oak', 'bush', 'pine', 'palm', 'bush'],
 ['oak', None, 'oak', 'pine', 'palm', None, None, 'pine', 'oak', None, 'oak', 'oak',
  'palm', 'pine', 'palm', 'oak', 'oak', 'pine', 'pine', 'oak'],
 ['pine', 'palm', None, 'oak', 'oak', 'oak', 'bush', 'pine', 'pine', 'bush', 'palm',
  'pine', 'palm', 'palm', 'pine', 'palm', 'palm', 'oak', None, 'oak'],
 ['oak', 'palm', 'oak', 'oak', 'bush', 'palm', 'pine', 'pine', 'palm', 'palm', None,
  'pine', 'oak', 'pine', 'bush', 'bush', 'pine', 'palm', 'oak', 'oak'],
 [None, None, 'pine', 'palm', 'palm', 'palm', None, 'palm', 'pine', 'palm', 'oak',
  'bush', None, 'palm', 'oak', 'palm', 'palm', 'palm', 'palm', 'pine'],
 ['palm', 'pine', None, 'bush', 'pine', None, 'oak', 'oak', 'bush', None, 'oak',
  'pine', 'oak', 'bush', None, 'palm', 'palm', 'bush', 'bush', 'bush'],
 ['palm', 'palm', 'pine', 'bush', None, 'bush', 'palm', 'bush', 'oak', 'bush',
  'pine', 'pine', 'pine', 'palm', None, 'pine', 'pine', None, 'pine', 'pine'],
 [None, 'bush', 'oak', 'oak', 'oak', 'bush', 'bush', 'pine', 'oak', 'oak', 'bush',
  'oak', 'palm', None, 'pine', 'palm', None, 'bush', 'pine', 'bush'],
 ['oak', 'bush', 'bush', 'palm', None, 'bush', 'palm', 'bush', 'bush', 'oak',
  'pine', 'palm', 'oak', 'palm', 'bush', 'pine', 'pine', 'pine', 'bush', 'palm'],
 ['oak', 'pine', 'oak', 'palm', 'palm', 'oak', 'pine', 'oak', None, 'oak', 'bush',
  'pine', 'oak', 'pine', 'bush', 'pine', 'oak', 'bush', 'palm', 'bush'],
 ['pine', 'bush', 'oak', None, 'bush', 'pine', None, 'oak', 'palm', 'pine', None,
  'oak', 'pine', None, 'bush', 'oak', 'pine', 'bush', 'palm', 'oak'],
 ['bush', 'pine', 'pine', 'pine', None, 'oak', None, 'bush', 'palm', 'palm', None,
  None, 'pine', None, 'bush', 'palm', 'bush', 'bush', 'pine', 'palm'],
 ['palm', 'palm', 'pine', 'oak', None, 'palm', 'oak', 'oak', 'palm', 'palm', 'pine',
  'pine', 'palm', 'oak', 'palm', None, 'palm', None, 'oak', None],
 ['palm', 'pine', 'palm', 'bush', None, None, 'oak', 'oak', 'oak', None, 'palm',
  'bush', 'oak', 'palm', 'oak', 'pine', None, 'palm', 'bush', 'pine'],
 ['oak', 'pine', None, None, None, None, None, 'bush', 'palm', 'oak', 'bush', 'bush',
  None, 'palm', 'oak', 'pine', None, 'bush', 'bush', 'oak'],
 ['bush', 'bush', 'oak', 'pine', 'palm', None, 'bush', 'pine', 'pine', 'bush',
  'oak', 'oak', 'oak', None, 'bush', 'bush', 'bush', 'bush', None, 'pine'],
 ['pine', 'oak', None, 'bush', None, 'oak', 'oak', 'pine', 'pine', None, 'palm',
  None, 'pine', 'pine', 'palm', 'bush', 'palm', 'palm', 'palm', 'pine'],
 [None, 'oak', 'oak', 'palm', None, 'oak', None, None, 'oak', None, 'palm', 'oak',
  'palm', None, 'oak', 'bush', None, 'bush', 'pine', 'pine'],
 ['bush', 'oak', 'bush', 'palm', None, None, None, None, None, 'oak', None, None,
  'oak', 'bush', None, 'bush', None, 'oak', 'pine', None],
 ['pine', 'oak', 'bush', 'pine', 'bush', None, None, None, 'oak', 'palm', 'palm',
  'oak', 'palm', 'oak', 'pine', None, None, None, 'pine', 'palm']])