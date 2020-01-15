import numpy as np

debug = False
filename = 'input24_2.txt' if debug else 'input24.txt'

with open(filename) as f:
  input_map = np.array([list(s.strip()) for s in f.readlines()])
  
input_map = input_map == "#"
map_size = input_map.shape[0]

def biodiversity(input_map):
  binary_biodev = np.reshape(input_map, [-1]).astype(np.int).tolist()
  
  return int(''.join([str(d) for d in binary_biodev[::-1]]), 2)

def update_map(input_map):
  next_map = np.copy(input_map)
  neigbor_count = np.zeros(input_map.shape)
  neigbor_count[:, :-1] += input_map[:, 1:]
  neigbor_count[:, 1:] += input_map[:, :-1]
  neigbor_count[:-1, :] += input_map[1:, :]
  neigbor_count[1:, :] += input_map[:-1, :]
  
  next_bug = np.logical_or(
      np.logical_and(input_map, neigbor_count == 1),
      np.logical_and(
          np.logical_and(~input_map, neigbor_count >= 1), neigbor_count <= 2)
      )
  next_map = next_bug
  
  return next_map
                     
  
def evolve_until_duplicate(input_map):
  biodev_ratings = {}
  while True:
    biodev_rating = biodiversity(input_map)
    if biodev_rating in biodev_ratings:
      return biodev_rating
    else:
      biodev_ratings[biodev_rating] = biodev_rating
      input_map = update_map(input_map)
      
def recursive_bug_count(depth, h, w, max_depth, all_maps):
  count = 0
  map_size = all_maps.shape[1]
  mid_pos = int(map_size // 2)
  
  if h == mid_pos and w == mid_pos:
    return 0
  
  # Higher level recursive count
  if depth > 0:
    count += all_maps[depth-1, mid_pos-1, mid_pos] if h == 0 else 0
    count += all_maps[depth-1, mid_pos+1, mid_pos] if h == map_size-1 else 0
    count += all_maps[depth-1, mid_pos, mid_pos-1] if w == 0 else 0
    count += all_maps[depth-1, mid_pos, mid_pos+1] if w == map_size-1 else 0
  
  # Direct neighbor count
  count += all_maps[depth, h-1, w] if h != 0 else 0
  count += all_maps[depth, h+1, w] if h != map_size-1 else 0
  count += all_maps[depth, h, w-1] if w != 0 else 0
  count += all_maps[depth, h, w+1] if w != map_size-1 else 0
  
  # Deeper level recursive count
  if depth+1 < all_maps.shape[0]:
    if h == mid_pos-1 and w == mid_pos:
      count += all_maps[depth+1, 0, :].sum()
    if h == mid_pos+1 and w == mid_pos:
      count += all_maps[depth+1, -1, :].sum()
    if h == mid_pos and w == mid_pos-1:
      count += all_maps[depth+1, :, 0].sum()
    if h == mid_pos and w == mid_pos+1:
      count += all_maps[depth+1, :, -1].sum()
  
  return count
      
def recursive_evolution(input_map, num_steps):
  max_depth = num_steps*2+1
  all_maps = np.zeros([max_depth] + list(input_map.shape)).astype(np.bool)
  all_maps[num_steps] = input_map
  map_size = input_map.shape[0]
  for i in range(num_steps):
#    print("Step {} of {}".format(i+1, num_steps))
    next_maps = np.zeros_like(all_maps)
    for j in range(max_depth):
      for h in range(map_size):
        for w in range(map_size):
          n_bug_count = recursive_bug_count(j, h, w, max_depth, all_maps)
          next_maps[j, h, w] = (all_maps[j, h, w] and n_bug_count == 1) or (
              ~all_maps[j, h, w] and (n_bug_count == 1 or n_bug_count == 2))
          
      
    all_maps = next_maps
      
  return all_maps.sum()
  
print("Part 1: {}".format(evolve_until_duplicate(input_map)))
if debug:
  print("Part 2: {}".format(recursive_evolution(input_map, 10)))
else:
  print("Part 2: {}".format(recursive_evolution(input_map, 200)))