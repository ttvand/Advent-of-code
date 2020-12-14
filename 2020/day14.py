import numpy as np


filename = 'input14.txt'
# filename = 'input14_2.txt'
# filename = 'input14_3.txt'

with open(filename) as f:
  data = [s.strip() for s in f.readlines()]
  
memory = {}
current_or_mask = 0
current_and_mask = 0
for d in data:
  if d[:4] == 'mask':
    or_mask = int(''.join(['1' if b == '1' else '0' for b in d[7:]]), 2)
    and_mask = int(''.join(['0' if b == '0' else '1' for b in d[7:]]), 2)
  else:
    parts = d.split('] = ')
    pos = int(parts[0][4:])
    value = int("{:036b}".format(int(parts[1])), 2)
    memory[pos] = (value & and_mask) | or_mask
    
print(sum([memory[k] for k in memory]))

###############################################################################

mask_val_writes = []
for d in data:
  if d[:4] == 'mask':
    mask = d[7:]
  else:
    parts = d.split('] = ')
    pos = "{:036b}".format(int(parts[0][4:]))
    value = int(parts[1])
    applied_mask = ''.join([p if m == '0' else m for (p, m) in zip(pos, mask)])
    mask_val_writes.append((applied_mask, value))
    
num_writes = len(mask_val_writes)
have_conflicts = np.zeros((num_writes, num_writes), dtype=np.bool)
for i in range(num_writes-1):
  for j in range(i+1, num_writes):
    count = ~np.any(np.array([(a == '1' and b == '0') or (
      a == '0' and b == '1') for (a, b) in zip(
        mask_val_writes[i][0], mask_val_writes[j][0])]))
    have_conflicts[i, j] = count
       
total_count = 0
for i in range(num_writes):
  conflict_ids = np.where(have_conflicts[i])[0]
  float_pos = [j for j, b in enumerate(mask_val_writes[i][0]) if b == 'X']
  num_floats = len(float_pos)
  valid_pos = np.ones(2**num_floats, dtype=np.bool)
  if conflict_ids.size:
    for c in conflict_ids:
      other_overwrite_ids = np.ones(2**num_floats, dtype=np.bool)
      for bit_id, fp in enumerate(float_pos):
        if mask_val_writes[c][0][fp] != 'X':
          bool_mask = np.repeat(
            np.array([True, False]), 2**(num_floats-1-bit_id))
          bool_mask = np.tile(bool_mask, 2**bit_id)
          overwrite_ids = bool_mask != (
            mask_val_writes[c][0][fp] == '0')
          other_overwrite_ids[overwrite_ids] = False
      valid_pos[other_overwrite_ids] = False
  
  total_count += valid_pos.sum() * mask_val_writes[i][1]
  
print(total_count)