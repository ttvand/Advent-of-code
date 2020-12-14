import numpy as np
part_2 = True

filename = 'input06.txt'
with open(filename) as f:
  data = [s.strip() for s in f.readlines()]
  
data += ['']
num_rows = len(data)
total_count = 0
group_vals = np.zeros(26, dtype=np.bool)
group_id = 0
for i in range(num_rows):
  if data[i] == '':
    total_count += group_vals.sum()
    # import pdb; pdb.set_trace()
    group_vals = np.zeros(26, dtype=np.bool)
    group_id = 0
    
  if part_2 and group_id > 0:
    for id_ in np.where(group_vals)[0]:
      if not chr(ord('a') + id_) in data[i]:
        group_vals[id_] = False
  else:
    for c in data[i]:
      group_vals[ord(c) - ord('a')] = True
      
  if data[i] != '':
    group_id += 1
    
print(total_count)