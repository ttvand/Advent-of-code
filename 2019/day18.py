import numpy as np

# filename = 'input18_2.txt'
filename = 'input18.txt'
with open(filename) as f:
  input_vals = np.array([[ord(e) for e in s.strip()] for s in f.readlines()])
with open(filename) as f:
  input_map = np.array([list(s.strip()) for s in f.readlines()])

current_pos = tuple([c[0] for c in np.where(input_map == "@")])
keys = np.sort(np.unique(input_map.flatten()[
    np.logical_and(97 <= input_vals.flatten(), input_vals.flatten() <= 122)]))
pos_dirs = {(-1, 0): 'U', (1, 0): 'D', (0, -1): 'L', (0, 1): 'R'}

# Find the shortest path from a position to all keys and keep track of the
# doors on that path
# Approach
def get_path_to_keys(pos, keys, grid):
    num_keys = len(keys)
    
    search_stack = [pos]
    shortest_paths = {pos: ('Source', 0)}
    
    while search_stack:
        search_pos = search_stack.pop()
        dist_to_start = shortest_paths[search_pos][1]
        for pos_dir in pos_dirs:
            next_pos = (search_pos[0] + pos_dir[0], search_pos[1] + pos_dir[1])
            if grid[next_pos[0], next_pos[1]] != '#':
                add_shortest_path = False
                if next_pos in shortest_paths:
                    next_distance = shortest_paths[next_pos][1]
                    add_shortest_path = dist_to_start + 1 < next_distance
                else:
                    add_shortest_path = True
                if add_shortest_path:
                    shortest_paths[next_pos] = (search_pos, dist_to_start + 1)
                    search_stack.append(next_pos)
                    
    paths = [pos] * num_keys
    path_details = []
    for (i, k) in enumerate(keys):
        key_pos = tuple([c[0] for c in np.where(input_map == k)])
        steps = [key_pos]
        if steps[-1] not in shortest_paths:
          continue
        while True:
            prev_step = shortest_paths[steps[-1]]
            if prev_step[0] == 'Source':
                steps = steps[::-1]
                break
                
            steps.append(prev_step[0])
            
        path_encodings = [grid[s[0], s[1]] for s in steps]
        keys_on_path = [s for s in path_encodings if 97 <= ord(s) <= 122]
        doors_on_path = [s for s in path_encodings if 65 <= ord(s) <= 90]
            
        paths[i] = steps
        path_details.append((''.join(keys_on_path),
                             ''.join(np.sort(doors_on_path)),
                             len(path_encodings)-1))
        
    
    return path_details
            
  
start_paths = get_path_to_keys(current_pos, keys, input_map)
shortest_key_paths = []
for (i, k) in enumerate(keys):
    key_pos = tuple([c[0] for c in np.where(input_map == k)])
    shortest_key_paths.append((str(k), get_path_to_keys(key_pos, keys, input_map)))
    
key_paths = []
for (k, d, l) in start_paths:
    if not d and len(k) == 1:
        key_paths.append(([k], l))
        
for i in range(len(keys)-1):
    # print(i, len(key_paths))
    next_key_paths = []
    for (k, l) in key_paths:
        match_key_id = np.where(keys == k[-1])[0][0]
        shortest_paths = shortest_key_paths[match_key_id][1]
        for (cons_key_id, cons_k) in enumerate(keys):
            new_keys = set(shortest_paths[cons_key_id][0]) - set(k)
            if not cons_k in k and len(new_keys) == 1:
                # Make sure no doors are obstructing the passage
                doors = shortest_paths[cons_key_id][1].lower()
                if not set(doors) - set(k):
                    path_len = shortest_paths[cons_key_id][2]
                    next_key_paths.append((k + [cons_k[-1]], l+path_len))
                    
    # Prune the paths - only keep the set with the lowest combined value
    # Caveat: only prune when the last key is identical!
    keep_next_paths = [True] * len(next_key_paths)
    path_distances = {}
    for (keep_id, (collected_keys, current_dist)) in enumerate(next_key_paths):
        original_keys = collected_keys.copy()
        prev_collected =  collected_keys[:-1].copy()
        prev_collected.sort()
        tuple_path = tuple(prev_collected + [collected_keys[-1]])
        if tuple_path in path_distances:
            (best_path_dist, best_path, prev_id) = path_distances[tuple_path]
            if current_dist < best_path_dist:
                path_distances[tuple_path] = (current_dist, original_keys, keep_id)
                keep_next_paths[prev_id] = False
            else:
                keep_next_paths[keep_id] = False
        else:
            path_distances[tuple_path] = (current_dist, original_keys, keep_id)
    
    next_key_paths = [p for (p, k) in zip(next_key_paths, keep_next_paths) if k]
    key_paths = next_key_paths

print("Part 1: {}".format(np.array([l for (_, l) in key_paths]).min()))

grid2 = input_map.copy()
grid2[39, 39:42] = ['@', '#', '@']
grid2[40, 39:42] = ['#', '#', '#']
grid2[41, 39:42] = ['@', '#', '@']
current_pos2 = [c for c in np.where(grid2 == "@")]
start_pos2 = [(current_pos2[0][i], current_pos2[1][i]) for i in range(4)]
start_paths = [get_path_to_keys(s, keys, grid2) for s in start_pos2]
shortest_key_paths = []
for (i, k) in enumerate(keys):
  key_pos = tuple([c[0] for c in np.where(grid2 == k)])
  shortest_key_paths.append((str(k), get_path_to_keys(key_pos, keys, grid2)))
  
key_paths = []
num_drones = 4
for i in range(num_drones):
  for (k, d, l) in start_paths[i]:
      if not d and len(k) == 1:
          drone_pos = ['Start']*num_drones
          drone_pos[i] = k
          key_paths.append(([k], l, drone_pos))
        
for i in range(len(keys)-1):
#  print(i, len(key_paths))
  next_key_paths = []
  for (k, l, drone_pos) in key_paths:
    for j in range(num_drones):
      if drone_pos[j] == 'Start':
        shortest_paths = start_paths[j]
      else:
        match_key_id = np.where(keys == drone_pos[j])[0][0]
        shortest_paths = shortest_key_paths[match_key_id][1]
      this_path_keys = [p[0][-1] for p in shortest_paths]
      for (cons_key_id, cons_k) in enumerate(this_path_keys):
        new_keys = set(shortest_paths[cons_key_id][0]) - set(k)
        if not cons_k in k and len(new_keys) == 1:
          # Make sure no doors are obstructing the passage
          doors = shortest_paths[cons_key_id][1].lower()
          if not set(doors) - set(k):
            path_len = shortest_paths[cons_key_id][2]
            new_drone_pos = drone_pos.copy()
            new_drone_pos[j] = cons_k
            next_key_paths.append((k + [cons_k], l+path_len, new_drone_pos))
                    
  # Prune the paths - only keep the set with the lowest combined value
  # Caveat: only prune when the last key is identical!
  keep_next_paths = [True] * len(next_key_paths)
  path_distances = {}
  for (keep_id, (collected_keys, current_dist, drone_pos)) in enumerate(
      next_key_paths):
      original_keys = collected_keys.copy()
      prev_collected =  collected_keys.copy()
      prev_collected.sort()
      tuple_path = tuple(prev_collected + drone_pos)
      if tuple_path in path_distances:
          (best_path_dist, prev_id) = path_distances[tuple_path]
          if current_dist < best_path_dist:
              path_distances[tuple_path] = (current_dist, keep_id)
              keep_next_paths[prev_id] = False
          else:
              keep_next_paths[keep_id] = False
      else:
          path_distances[tuple_path] = (current_dist, keep_id)
  
  next_key_paths = [p for (p, k) in zip(next_key_paths, keep_next_paths) if k]
  key_paths = next_key_paths

print("Part 2: {}".format(np.array([l for (_, l, _) in key_paths]).min()))