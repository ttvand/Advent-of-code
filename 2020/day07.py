import numpy as np

filename = '../../Downloads/input07.txt'
with open(filename) as f:
  data = [s for s in f.readlines()]

contents = {}
no_other_bags = []
for l in data:
  parts = l.split(" contain ")
  content_parts_raw = parts[1][:-2].split(", ")
  if parts[1][:-2] == "no other bags":
    no_other_bags.append(parts[0][:-5])
    content_parts = None
  else:
    content_parts = [(int(cp[0]), cp[2:]) for cp in content_parts_raw]
    content_parts = [(a, b[:-4]) if a == 1 else (a, b[:-5]) for (
      a, b) in content_parts]
  contents[parts[0][:-5]] = content_parts
  
valid_added = []
valid_considered = ['shiny gold']

while True:
  num_added = 0
  for c in contents:
    cont = contents[c]
    if not c in valid_considered and not cont is None:
      valid = False
      for (_, b) in cont:
        if b in valid_considered:
          valid = True
          break
      if valid:
        valid_added.append(c)
        
  if valid_added:
    valid_considered += valid_added
    valid_added = []
  else:
    break
  
bag_counts = {}
for b in no_other_bags:
  bag_counts[b] = 1
  
while not 'shiny gold' in bag_counts:
  for k in contents:
    if not k in bag_counts:
      cont = contents[k]
      all_keys_present = True
      for _, b in cont:
        all_keys_present = all_keys_present and b in bag_counts
      
      if all_keys_present:
        total_count = 1
        for n, b in cont:
          total_count += n*bag_counts[b]
        bag_counts[k] = total_count

print(bag_counts['shiny gold']-1)