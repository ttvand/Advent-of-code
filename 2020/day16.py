import numpy as np


filename = 'input16.txt'; num_fields = 20
# filename = 'input16_2.txt'; num_fields = 3

with open(filename) as f:
  data = [s.strip() for s in f.readlines()]
  
# Process input data
inputs = {}
for i in range(num_fields):
  parts = data[i].split(': ')
  ranges = np.array(
    [[int(sr) for sr in r.split('-')] for r in parts[1].split(' or ')])
  inputs[parts[0]] = ranges

my_ticket = np.array([int(d) for d in data[num_fields+2].split(',')])
other_tickets = []
for d in data[(num_fields+5):]:
  other_tickets.append(np.array([int(sd) for sd in d.split(',')]))

# Part 1
flat_others = np.stack(other_tickets).flatten()
all_input_ranges = np.concatenate(
  [flat_others, np.stack(list(inputs.values())).flatten()])
valid_ranges = np.zeros(all_input_ranges.max()+1, dtype=np.bool)
for k in inputs:
  for j in range(2):
    valid_ranges[inputs[k][j][0]:(inputs[k][j][1]+1)] = True
invalid_others = flat_others[~valid_ranges[flat_others]]
print(invalid_others.sum())

# Part 2
others_valid = np.stack(
  [o for o in other_tickets if np.all(valid_ranges[o.flatten()])])
input_keys = list(inputs.keys())
num_keys = len(input_keys)
valid_ranges = np.zeros((all_input_ranges.max()+1, num_keys), dtype=np.bool)
for i in range(num_keys):
  valid_ranges[others_valid[:, i], i] = True
  
# Row: True index
# Col: ticket index
valid_orders = np.ones((num_keys, num_keys), dtype=np.bool)
for i in range(num_keys):
  vals = others_valid[:, i]
  for j in range(num_keys):
    ranges = inputs[input_keys[j]]
    valid_orders[j, i] = np.all(
      ((vals >= ranges[0][0]) & ((vals <= ranges[0][1]))) | (
        (vals >= ranges[1][0]) & ((vals <= ranges[1][1]))))

col_assignment = {}
already_assigned = np.zeros(num_keys)
vo = np.copy(valid_orders)
for _ in range(num_fields):
  assign_id = np.argmin(vo.sum(1) + 100*already_assigned)
  assert vo[assign_id].sum() == 1
  assert (vo.sum(1) == 1).sum() == 1
  assign_order = np.where(vo[assign_id])[0][0]
  col_assignment[assign_id] = assign_order
  vo[assign_id] = False
  vo[:, assign_order] = False
  already_assigned[assign_id] = True

departure_fields = np.array([
  col_assignment[i] for i, k in enumerate(input_keys) if 'departure' in k])
print(np.prod(my_ticket[departure_fields]))
