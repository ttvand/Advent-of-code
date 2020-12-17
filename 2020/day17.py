import numpy as np
from scipy.ndimage import convolve


filename = 'input17.txt'
# filename = 'input17_2.txt'

with open(filename) as f:
  data = np.array([[c == '#' for c in s.strip()] for s in f.readlines()])
  
def conway(dim):
  k = np.ones(tuple([3]*dim))
  k[tuple([1]*dim)] = 0
  nr = data.shape[0]
  sr1 = nr*2
  sr2 = nr
  
  inputs = np.zeros(tuple([nr*4]*2+[nr*2 for _ in range(dim-2)])).astype(bool)
  if dim == 3:
    inputs[sr1:sr1+data.shape[0], sr1:sr1+data.shape[1], sr2] = data
  else:
    inputs[sr1:sr1+data.shape[0], sr1:sr1+data.shape[1], sr2, sr2] = data
    
  for _ in range(6):
    neighbor_count = convolve(inputs.astype(np.int), k, mode='constant')
    inputs = (inputs & (neighbor_count == 2)) | (neighbor_count == 3)
    
  print(inputs.sum())
  
conway(3); conway(4)