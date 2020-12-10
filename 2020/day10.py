import numpy as np

filename = '../../Downloads/input10.txt'
# filename = '../../Downloads/input10-2.txt'

with open(filename) as f:
  data = np.array([int(s) for s in f.readlines()])

assert data.size == np.unique(data).size
sd = np.sort(data)

one_diff_count = 0
three_diff_count = 0

sda = np.array([0] + sd.tolist() + [sd[-1]+3])
num_numbers = sda.size
sdad = np.diff(sda)
print((sdad==1).sum()*(sdad==3).sum())

def num_sols(i, n, sols):
  # print(i, n)
  if n in sols:
    return sols[n]
  else:
    total = 0
    incr_id = 1
    for j in range(1, 4):
      next_id = i + incr_id
      if sda[next_id] == n+j:
        total += num_sols(next_id, n+j, sols)
        incr_id += 1
    sols[n] = total
    return total
    
print(num_sols(0, sda[0], {sda[-1]: 1}))