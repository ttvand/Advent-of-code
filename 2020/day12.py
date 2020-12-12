import numpy as np

filename = 'input12.txt'
# filename = 'input12_2.txt'

with open(filename) as f:
  data = [s for s in f.readlines()]
  data_parts = [(d[0], int(d[1:])) for d in data]

rot_dirs = ['N', 'E', 'S', 'W']
directions = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
directions = {k: np.array(v) for k, v in directions.items()}

pos = np.array([0, 0])
positions = [np.copy(pos)]
rot_dir = 1
for com, val in data_parts:
  if com == 'F':
    move_val = val * directions[rot_dirs[rot_dir]]
  elif com in 'NESW':
    move_val = val * directions[com]
  elif com in 'LR':
    rot_dir = (rot_dir + val//90*(-1 if com == 'L' else 1)) % 4
    move_val = np.array([0, 0])
    
  pos += move_val
  positions.append(np.copy(pos))
    
print(np.abs(positions[-1]).sum())

###############################################################

ship_pos = np.array([0, 0])
way_pos = np.array([10, 1])
ship_positions = [np.copy(ship_pos)]
way_positions = [np.copy(way_pos)]
rot_m = {d: np.array([[np.cos(d/180*np.pi), -np.sin(d/180*np.pi)],
                      [np.sin(d/180*np.pi), np.cos(d/180*np.pi)]]) for d in [
                        90, 180, 270]}
for com, val in data_parts:
  ship_move_val = np.array([0, 0])
  way_move_val = np.array([0, 0])
  if com == 'F':
    ship_move_val = val * way_pos
  elif com in 'NESW':
    way_move_val = val * directions[com]
  elif com in 'LR':
    rot_degrees = val*(-1 if com == 'R' else 1) % 360
    rel_rot_pos = np.round(np.matmul(
      rot_m[rot_degrees], way_pos.reshape((-1, 1)))[:, 0]).astype(np.int)
    way_move_val = rel_rot_pos - way_pos
    move_val = np.array([0, 0])
    
  ship_pos += ship_move_val
  way_pos += way_move_val
  ship_positions.append(np.copy(ship_pos))
  way_positions.append(np.copy(way_pos))
  
print(np.abs(ship_positions[-1]).sum())