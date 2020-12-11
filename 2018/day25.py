import numpy as np

filename = 'input25.txt'

with open(filename) as f:
  data = np.array([[int(s) for s in l.split(",")] for l in (
    f.readlines())])
  
distances = np.abs(data[None] - data[:, None]).sum(-1)
num_units = distances.shape[0]

const_counts = 0
covered = np.zeros(num_units, dtype=np.bool)
while not np.all(covered):
  covered_this_constellation = np.zeros(num_units, dtype=np.bool)
  first_not_covered = np.where(~covered)[0][0]
  covered_this_constellation[first_not_covered] = True
  while not np.all(covered):
    check_dims = (~covered_this_constellation) & (~covered)
    min_distances = distances[
      covered_this_constellation][:, check_dims].min(0)
    new_ids = np.where(check_dims)[0][min_distances <= 3]
    if new_ids.size == 0:
      break
    covered_this_constellation[new_ids] = True
  covered[covered_this_constellation] = True
  const_counts += 1
  
print(const_counts)