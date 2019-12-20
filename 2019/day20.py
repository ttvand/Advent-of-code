import numpy as np

# filename = 'input18_2.txt'
filename = 'input20.txt'
with open(filename) as f:
  input_map = np.array([list(s) for s in f.readlines()])
  
# Locate all portals