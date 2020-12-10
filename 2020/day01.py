import numpy as np

filename = '../../Downloads/input01.txt'
with open(filename) as f:
  data = np.array([int(s.strip()) for s in f.readlines()])

for i, d in enumerate(data):
  v = 2020-d
  if v in data[:max(0, i-1)]:
    print(d*v)
    
num_entries = data.size
for i in range(num_entries-2):
  for j in range(i+1, num_entries-1):
    v = 2020 - data[i] - data[j]
    if v in data:
      print(v*data[i]*data[j])