import numpy as np

filename = '../../Downloads/input09.txt'
preamble = 25

# filename = '../../Downloads/input09_2.txt'
# preamble = 5

with open(filename) as f:
  data = np.array([int(s) for s in f.readlines()])

num_data = len(data)
for i in range(preamble, num_data):
  number = data[i]
  matches = []
  for j in range(i-preamble, i):
    valid = False
    if data[j] in matches:
      valid = True
      break
    else:
      matches.append(data[i] - data[j])
  
  if not valid:
    inv = data[i]
    break
  
print(inv)

start_id = 0
range_sum = data[0]
for j in range(1, num_data):
  while range_sum > inv:
    range_sum -= data[start_id]
    start_id += 1
    
  if range_sum == inv:
    print(data[start_id:j].min() + data[start_id:j].max())
    break
    
  range_sum += data[j]