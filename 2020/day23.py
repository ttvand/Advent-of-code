import copy
import numpy as np


nrounds_1 = 100
nrounds_2 = int(1e7)
max_cup_2 = int(1e6)
labeling = ['389125467', '712643589', '289154673'][0]

# Parse the input
cups = [int(c) for c in labeling]

# Part 1
for _ in range(nrounds_1):
  cur_val = cups[0]
  min_other = min(cups[4:])
  if min_other <= cur_val-1:
    target = max([c for c in cups[4:] if c < cur_val])
  else:
    target = max(cups[4:])
  
  dest = 4
  while True:
    if cups[dest] == target:
      cups = cups[4:dest+1] + cups[1:4] + cups[dest+1:] + cups[:1]
      break
    else:
      dest += 1
      
one_pos = np.where(np.array(cups) == 1)[0][0]
cups_s = [str(c) for c in cups]
print(''.join(cups_s[one_pos+1:] + cups_s[:one_pos]))

# # Part 2 smart force (cyclic linked list - incomplete)
# class Node:
#   def __init__(self, val, prev, nxt):
#     self.val = val
#     self.prev = prev
#     self.nxt = nxt

# cups = np.concatenate([
#   np.array([int(c) for c in labeling]),
#   1+np.arange(len(cups), int(max_cup_2))])
# nodes = [Node(c, None, None) for c in cups]
# val_pos = {}
# for i in range(max_cup_2):
#   nodes[i].prev = nodes[(i-1) % max_cup_2]
#   nodes[i].nxt = nodes[(i+1) % max_cup_2]
#   val_pos[cups[i]] = i

# cur_val = cups[0]
# cur_pos = 0
# for round_2 in range(nrounds_2):
#   cons_val = cur_val-1
  
#   while True:
#     pos_diff = (val_pos[cons_val] - cur_pos) % max_cup_2
#     if pos_diff <= 3:
#       if cons_val > 1:
#         cons_val -= 1
#       else:
#         cons_val = max_cup_2
#     else:
#       dest = val_pos[cons_val]
#       break
  
#   # nodes[cur_pos].nxt = nodes[cur_pos].nxt.nxt.nxt.nxt
#   # nodes[dest].nxt = nodes[cur_pos].nxt
#   # nodes[cur_pos].nxt.nxt.nxt = nodes[dest].nxt
#   a = copy.copy(nodes[cur_pos].nxt.nxt.nxt.nxt)
#   b = copy.copy(nodes[cur_pos].nxt.nxt.nxt)
#   c = copy.copy(nodes[cur_pos].nxt)
#   d = copy.copy(nodes[dest].nxt)
  
#   nodes[cur_pos].nxt = a
#   nodes[dest].nxt = c
#   b.nxt = d
  
#   cur_pos = dest
  
#   if round_2 % 10000 == 0:
#     print(f"Progress: {round_2/100000}%")

# final = []
# n = nodes[dest]
# for _ in range(max_cup_2):
#   final.append(n.val)
#   n = n.nxt
# print(final)

# Part 2 brute force
cups = np.concatenate([
  np.array([int(c) for c in labeling]),
  1+np.arange(len(cups), int(max_cup_2))])

for round_2 in range(nrounds_2):
  cur_val = cups[0]
  if cur_val > 1 and not np.any(cups[1:4] == (cur_val-1)):
    target = cur_val-1
  else:
    min_other = cups[4:].min()
    if min_other <= cur_val-1:
      target = cups[4:][cups[4:] < cur_val].max()
    else:
      target = cups[4:].max()
  
  dest = 4+np.argmax(cups[4:] == target)
  
  # # Concatenate approach
  # cups = np.concatenate([cups[4:dest+1], cups[1:4], cups[dest+1:], cups[:1]])
  
  # Val copy approach (about 2/3 of the execution time of the concat approach)
  first_vals = np.copy(cups[:4])
  cups[:dest-3] = cups[4:dest+1]
  cups[dest-3:dest] = first_vals[1:4]
  cups[dest:-1] = cups[dest+1:]
  cups[-1] = first_vals[0]
  
  if round_2 % 10000 == 0:
    print(f"Progress: {round_2/100000}%")
    
one_pos = np.where(np.array(cups) == 1)[0][0]
print(np.prod(np.concatenate([cups[one_pos+1:], cups[:2]])[:2]))