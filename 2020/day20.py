import numpy as np


filename = 'input20.txt'
# filename = 'input20_2.txt'

with open(filename) as f:
  data = [d.strip() for d in f.readlines()]
  
# Parse the inputs
id_ = 0
tile_mappings = {}
tiles = []
tile_id = 0
while id_+10 < len(data):
  tile = int(data[id_].split(' ')[1][:-1])
  vals = np.array([[c == '#' for c in data[r]] for r in range(id_+1, id_+11)])
  tiles.append(vals)
  tile_mappings[tile_id] = tile
  id_ += 12
  tile_id += 1

def get_border_id(tile, id_):
  if id_ == 0:
    return tile[0]
  elif id_ == 1:
    return tile[:, -1]
  elif id_ == 2:
    return tile[-1]
  else:
    return tile[:, 0]

# Compute the possible alignments of squares
num_tiles = len(tiles)
image_dim = int(np.sqrt(len(tiles)))
aligns = np.zeros((num_tiles, num_tiles, 32), dtype=np.bool)
for i in range(num_tiles-1):
  for j in range(i+1, num_tiles):
    for first_border_id in range(4):
      first = get_border_id(tiles[i], first_border_id)
      for k in range(8):
        second = get_border_id(tiles[j], k % 4)
        if k//4 == 1:
          second = np.flip(second)
        
        match = np.all(first == second)
        match_pos_first = first_border_id*8+k
        match_pos_second = (k%4)*8 + first_border_id+4*int(k//4 == 1)
        aligns[i, j, match_pos_first] = match
        aligns[j, i, match_pos_second] = match
      
# Part 1: corner pieces only have two matching neighbors
corner_pieces = np.where(aligns.sum((1, 2)) == 2)[0]
print(np.prod(np.array([tile_mappings[p] for p in corner_pieces])))
      
# Part 2: compose the puzzle
...

# # Pick a tile with 4 matches (a non edge piece) and then then connect pieces to 
# # a random tile that can still be connected with other pieces
# central_pieces = np.where(aligns.sum((1, 2)) == 4)[0]
# first_piece = central_pieces[0]
# pieces = {first_piece: 0}
# assigned = np.zeros(num_tiles, dtype=np.bool)
# assigned[first_piece] = True
# while not np.all(assigned):
#   assigned_ids = np.where(assigned)[0]
#   match_current = aligns[:, assigned].sum(-1).flatten()*(~assigned)
  
#   # Decide on the orientation and rotation of the assigned piece
#   assign_id = np.where(match_current)[0][0]
#   constraints = np.where(aligns[assign_id, assigned])
#   for i in range(constraints[0].size):
#     other_id = assigned_ids[constraints[0][i]]
#     other_rel_orientation = constraints[1][i]
#     other_orientation = pieces[other_id]
#     import pdb; pdb.set_trace()
#     x=1
  
#   assigned[assign_id] = True