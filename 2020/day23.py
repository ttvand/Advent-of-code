import copy
import numpy as np


nrounds_1 = 100
nrounds_2 = int(1e7)
max_cup_2 = int(1e6)
labeling = ['389125467', '712643589'][1]

# Parse the input
cups = [int(c) for c in labeling]

# Part 1
for _ in range(nrounds_1):
  cur_val = cups[0]
  min_other = min(cups[4:])
  if min_other <= cur_val-1:
    target = max([c for c in cups[4:] if c < cur_val])
  else:
    target = max(cups[4:])
  
  dest = 4
  while True:
    if cups[dest] == target:
      cups = cups[4:dest+1] + cups[1:4] + cups[dest+1:] + cups[:1]
      break
    else:
      dest += 1
      
one_pos = np.where(np.array(cups) == 1)[0][0]
cups_s = [str(c) for c in cups]
print(''.join(cups_s[one_pos+1:] + cups_s[:one_pos]))

# Part 2
cups = np.concatenate([
  np.array([int(c) for c in labeling]),
  1+np.arange(len(cups), int(max_cup_2))])

for round_2 in range(nrounds_2):
  cur_val = cups[0]
  if cur_val > 1 and not np.any(cups[1:4] == (cur_val-1)):
    target = cur_val-1
  else:
    min_other = cups[4:].min()
    if min_other <= cur_val-1:
      target = cups[4:][cups[4:] < cur_val].max()
    else:
      target = cups[4:].max()
  
  dest = 4+np.argmax(cups[4:] == target)
  
  # # Concatenate approach
  # cups = np.concatenate([cups[4:dest+1], cups[1:4], cups[dest+1:], cups[:1]])
  
  # Val copy approach (about 2/3 of the execution time of the concat approach)
  first_vals = np.copy(cups[:4])
  cups[:dest-3] = cups[4:dest+1]
  cups[dest-3:dest] = first_vals[1:4]
  cups[dest:-1] = cups[dest+1:]
  cups[-1] = first_vals[0]
  
  if round_2 % 10000 == 0:
    print(f"Progress: {round_2/100000}%")
    
one_pos = np.where(np.array(cups) == 1)[0][0]
print(np.prod(np.concatenate([cups[one_pos+1:], cups[:2]])[:2]))