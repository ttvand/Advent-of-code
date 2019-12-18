import numpy as np

filename = 'input18.txt'
with open(filename) as f:
  input_vals = np.array([[ord(e) for e in s.strip()] for s in f.readlines()])
with open(filename) as f:
  input_map = np.array([list(s.strip()) for s in f.readlines()])

map_dim = input_map.shape[0]
current_pos = [c[0] for c in np.where(input_map == "@")]
keys = np.sort(np.unique(input_map.flatten()[
    np.logical_and(97 <= input_vals.flatten(), input_vals.flatten() <= 122)]))