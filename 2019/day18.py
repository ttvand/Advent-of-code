import numpy as np

filename = 'input18.txt'
with open(filename) as f:
  input_vals = np.array([[ord(e) for e in s.strip()] for s in f.readlines()])
with open(filename) as f:
  input_map = np.array([list(s.strip()) for s in f.readlines()])

map_dim = input_map.shape[0]
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
        print(search_pos)
        for pos_dir in pos_dirs:
            next_pos = (search_pos[0] + pos_dir[0], search_pos[1] + pos_dir[1])
            if grid[next_pos[0], next_pos[1]] != '#':
                if next_pos in shortest_paths:
                    next_distance = shortest_paths[next_pos][1]
                    if dist_to_start + 1 < next_distance:
                        import pdb; pdb.set_trace()
                        x=1
                else:
                    shortest_paths[next_pos] = (search_pos, dist_to_start + 1)
                    search_stack.append(next_pos)
                    
    paths = [pos] * num_keys
    keys_and_doors = [''] * num_keys
    for (i, k) in enumerate(keys):
        key_pos = tuple([c[0] for c in np.where(input_map == k)])
        steps = [key_pos]
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
        keys_and_doors[i] = (''.join(np.sort(keys_on_path)),
                             ''.join(np.sort(doors_on_path)))
        
    
    import pdb; pdb.set_trace()
    x=1
            
  
doors_on_pathcurrent_to_keys = get_path_to_keys(current_pos, keys, input_map)
  