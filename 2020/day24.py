import copy
import numpy as np


filename = 'input24.txt'
# filename = 'input24_2.txt'

num_days_2 = 100

with open(filename) as f:
  data = [d.strip() for d in f.readlines()]

# Move directions:  e, se, sw, w, nw, and ne
pos_change = {'e': (2, 0), 'se': (1, -1), 'sw': (-1, -1), 'w': (-2, 0),
              'nw': (-1, 1), 'ne': (1, 1)}
directions = []
for d in data:
  one_dir = []
  id_ = 0
  while id_ < len(d):
    if d[id_] in ['e', 'w']:
      one_dir.append(d[id_])
      id_ += 1
    else:
      one_dir.append(d[id_:id_+2])
      id_ += 2
  directions.append(one_dir)
  
tiles = {}
for d in directions:
  pos = [0, 0]
  for s in d:
    change = pos_change[s]
    pos[0] += change[0]
    pos[1] += change[1]
  
  pos_k = tuple(pos)
  if pos_k in tiles:
    tiles[pos_k] = not tiles[pos_k]
  else:
    tiles[pos_k] = False
    
print(0, (~np.array(list(tiles.values()))).sum())

def get_neighbors(t):
  neighbors = []
  for v in pos_change.values():
    neighbors.append((t[0] + v[0], t[1] + v[1]))
    
  return neighbors

# Only keep track of black tiles (everything unspecified is white)
blacks = set([k for k, v in tiles.items() if not v])
for i in range(num_days_2):
  # Neighbor count
  neighbors = {}
  for b in blacks:
    for n in get_neighbors(b):
      if n in neighbors:
        neighbors[n] += 1
      else:
        neighbors[n] = 1
        
  # B -> W transitions: not 1 or 2 B neighbors
  just_flipped = set()
  for b in list(blacks):
    if not b in neighbors or not neighbors[b] in [1, 2]:
      blacks.remove(b)
      just_flipped.add(b)
  
  # W -> B transitions: 2 B neighbors and not flipped in this round
  # import pdb; pdb.set_trace()
  white_to_black = set()
  for k in [k for k, v in neighbors.items() if v == 2]:
    if k not in blacks and k not in just_flipped:
      white_to_black.add(k)
  
  blacks = blacks.union(white_to_black)
  print(i+1, len(blacks))