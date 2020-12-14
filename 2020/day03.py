import numpy as np

filename = 'input03.txt'
with open(filename) as f:
  data = np.array([s.strip() for s in f.readlines()])
  
def slope_func(r, c):
  tree_count = 0
  col_id = 0
  num_cols = len(data[0])
  for r in range(r, len(data), r):
    col_id = (col_id + c) % num_cols
    tree_count += (data[r][col_id] == '#')
  
  return tree_count
  
print(slope_func(1, 3))

print(np.prod([
  slope_func(1, 1),
  slope_func(1, 3),
  slope_func(1, 5),
  slope_func(1, 7),
  slope_func(2, 1),
  ]))
  