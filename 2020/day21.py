import numpy as np


filename = 'input21.txt'
# filename = 'input21_2.txt'

with open(filename) as f:
  data = [d.strip() for d in f.readlines()]
  
# Extract the inputs
inputs = []
for d in data:
  parts = d.split(' (contains ')
  inputs.append((parts[1][:-1].split(', '), parts[0].split(' ')))
  
allergens = list(set([e for a in inputs for e in a[0]]))
foods = list(set([e for a in inputs for e in a[1]]))
fids = {f: i for i, f in enumerate(foods)}

matches = np.zeros((len(allergens), len(foods)), dtype=np.bool)
for a_id, a in enumerate(allergens):
  matching_eqs = np.array([i for (i, inp) in enumerate(inputs) if (
    a in inp[0])])
  food = set.intersection(*[set(inputs[eq_id][1]) for eq_id in matching_eqs])
  f_ids = np.array([fids[f] for f in food])
  matches[a_id, f_ids] = True
  
# Part 1: list the no allergen foods
no_a_foods = [foods[i] for i in np.where(matches.sum(0) == 0)[0]]
no_a_count = np.array([int(e in no_a_foods) for a in inputs for e in a[1]])
print(no_a_count.sum())

exact_a = {}
while matches.sum():
  unique_ids = np.where(matches.sum(0) == 1)[0]
  f_id = unique_ids[0]
  i_id = np.where(matches[:, f_id])[0]
  exact_a[allergens[i_id[0]]] = foods[f_id]
  
  matches[:, f_id] = False
  matches[i_id] = False
  
r = [x for _, x in sorted(zip(list(exact_a.keys()), list(exact_a.values())))]
print(','.join(r))