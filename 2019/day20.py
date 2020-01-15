import numpy as np

# filename = 'input20_2.txt'
filename = 'input20.txt'
with open(filename) as f:
  input_map = np.array([list(s) for s in f.readlines()])
  
# Locate all portals
def is_capital(c):
    return c >= 'A' and c <= 'Z'
num_rows = input_map.shape[0]
num_cols = input_map.shape[1]
start_rows = [(0, 2), (31, -1), (86, 2), (117, -1)]
start_cols = [(0, 2), (31, -1), (84, 2), (115, -1)]
portal_positions = {}
portal_connections = {}
for (start_row, portal_offset) in start_rows:
    for i in range(num_cols):
        first_char = input_map[start_row, i]
        if is_capital(first_char):
            second_char = input_map[start_row+1, i]
            if is_capital(second_char):
                portal = first_char[0] + second_char[0]
                portal_pos = (start_row + portal_offset, i)
                if portal in portal_positions:
                    other_portal_pos = portal_positions[portal]
                    portal_connections[portal_pos] = other_portal_pos
                    portal_connections[other_portal_pos] = portal_pos
                else:
                    portal_positions[portal] = portal_pos
for (start_col, portal_offset) in start_cols:
    for i in range(num_rows):
        first_char = input_map[i, start_col]
        if is_capital(first_char):
            second_char = input_map[i, start_col+1]
            if is_capital(second_char):
                portal = first_char[0] + second_char[0]
                portal_pos = (i, start_col + portal_offset)
                if portal in portal_positions:
                    other_portal_pos = portal_positions[portal]
                    portal_connections[portal_pos] = other_portal_pos
                    portal_connections[other_portal_pos] = portal_pos
                else:
                    portal_positions[portal] = portal_pos

# BFS to find shortest path from AA to ZZ
start_pos = portal_positions['AA']
terminal_pos = portal_positions['ZZ']
considered_pos = [start_pos]
offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), None]
step_counter = 0
visited = [start_pos]
exit_search = False
while not exit_search:
#    print(step_counter, len(considered_pos), considered_pos)
    step_counter += 1
    next_considered_pos = []
    for pos in considered_pos:
        for (i, offset) in enumerate(offsets):
            if i == 4:
                valid_move = pos in portal_connections
                next_pos = portal_connections[pos] if valid_move else None
            else:
                next_pos = (pos[0] + offsets[i][0], pos[1] + offsets[i][1])
                valid_move = input_map[next_pos[0], next_pos[1]] == '.'
            if valid_move and not next_pos in visited:
                next_considered_pos.append(next_pos)
                visited.append(next_pos)
                
            if next_pos == terminal_pos:
                exit_search = True
                
    considered_pos = next_considered_pos

print("Part 1:", step_counter)


# BFS to find shortest path from AA to ZZ, while keeping track of the depth of the maze
terminal_pos_2 = tuple(list(terminal_pos) + [0])
considered_pos = [tuple(list(start_pos) + [0])]
offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), None]
step_counter = 0
visited = {tuple(list(start_pos) + [0]): True}
exit_search = False
max_depth = 50 # Heuristic to speed up search - increase if no solutions are found
while not exit_search:
    # print(step_counter, len(considered_pos), considered_pos)
#    print(step_counter, len(considered_pos))
    step_counter += 1
    next_considered_pos = []
    for pos_depth in considered_pos:
        pos = pos_depth[:2]
        depth = pos_depth[2]
        for (i, offset) in enumerate(offsets):
            if i == 4:
                valid_move = pos in portal_connections
                inner_portal = pos[0] > 3 and pos[0] < 100 and pos[1] > 3 and pos[1] < 100
                valid_move = valid_move and (inner_portal or depth > 0)
                next_depth = depth + 1 if inner_portal else depth - 1
                valid_move = valid_move and next_depth <= max_depth
                next_pos = tuple(list(portal_connections[pos]) + [next_depth]) if (
                    valid_move) else None
            else:
                next_pos = (pos[0] + offsets[i][0], pos[1] + offsets[i][1], depth)
                valid_move = input_map[next_pos[0], next_pos[1]] == '.'
            if valid_move and not next_pos in visited:
                next_considered_pos.append(next_pos)
                visited[next_pos] = True
                
            if next_pos == terminal_pos_2:
                exit_search = True
                
    considered_pos = next_considered_pos

print("Part 2:", step_counter)