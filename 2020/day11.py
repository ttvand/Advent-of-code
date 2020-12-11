import numpy as np
from scipy.signal import convolve2d

filename = 'input11.txt'
# filename = 'input11_2.txt'

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

with open(filename) as f:
  is_seat = np.array([[ss == 'L' for ss in s[:-1]] for s in f.readlines()])

occupied = np.zeros_like(is_seat)
neighbor_mask = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

prev_occupied =  ~occupied
while not np.all(occupied == prev_occupied):
  occ_count = convolve2d(occupied, neighbor_mask, mode='same')
  become_occupied = is_seat & (~occupied) & (occ_count == 0)
  become_unoccupied = is_seat & occupied & (occ_count >= 4)
  
  prev_occupied = np.copy(occupied)
  occupied[become_occupied] = True
  occupied[become_unoccupied] = False
  
print(occupied.sum())

can_see_pos = {}
for i in range(occupied.shape[0]):
  for j in range(occupied.shape[1]):
    considered_seats = []
    for d in DIRS:
      move_id = 1
      while True:
        cons_pos = (i+d[0]*move_id, j+d[1]*move_id)
        if cons_pos[0] < 0 or cons_pos[0] >= occupied.shape[0] or (
            cons_pos[1] < 0) or cons_pos[1] >= occupied.shape[1]:
          break
        elif is_seat[cons_pos]:
          considered_seats.append(cons_pos)
          break
        else:
          move_id += 1 
    can_see_pos[(i, j)] = tuple([np.array(e) for e in zip(*considered_seats)])
    
occupied = np.zeros_like(is_seat)

prev_occupied =  ~occupied
while not np.all(occupied == prev_occupied):
  occ_count = np.array([[occupied[can_see_pos[i, j]].sum() for j in range(
    occupied.shape[1])] for i in range(occupied.shape[0])])
  become_occupied = is_seat & (~occupied) & (occ_count == 0)
  become_unoccupied = is_seat & occupied & (occ_count >= 5)
  
  prev_occupied = np.copy(occupied)
  occupied[become_occupied] = True
  occupied[become_unoccupied] = False
  
print(occupied.sum())