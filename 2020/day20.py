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
      

def get_transformations(tile):
  trans = []
  for f in [False, True]:
    if f:
      tile = np.flip(tile, 1)
    for i in range(4):
      trans.append(tile)
      tile = np.rot90(tile)
  
  return trans

def connect(i, j, grid):
  if j == 0:
    tile, trans, tile_id = grid[i-1][j]
    order = 'up'
    ref_border = trans[-1] 
  else:
    tile, trans, tile_id = grid[i][j-1]
    order = 'left'
    ref_border = trans[:, -1] 
  
  tiles_in_use = np.array([g[2] for r in grid for g in r if g is not None])
  considered_new = np.setdiff1d(
    np.where(aligns[tile_id].sum(-1) > 0)[0], np.array(tiles_in_use))
  
  for n in considered_new:
    for t in all_trans[n]:
      new_border = t[0] if order == 'up' else t[:, 0]
      
      if np.all(new_border == ref_border):
        grid[i][j] = (tiles[n], t, n)
        return True
      
  return False

all_trans = [get_transformations(t) for t in tiles]

# Part 2: compose the puzzle: start in the top left and go right - down.
# Try all possible transformations for the first corner 
first_corner_piece = corner_pieces[0]
for t in all_trans[first_corner_piece]:
  grid = [[None for _ in range(image_dim)] for _ in range(image_dim)]
  grid[0][0] = (all_trans[first_corner_piece][0], t, first_corner_piece)
  success = True
  for i in range(image_dim):
    for j in range(image_dim):
      if grid[i][j] is None:
        can_connect = connect(i, j, grid)
        if not can_connect:
          success = False
          break
    if not success:
      break
        
  if success:
    break
  
puzzle = np.concatenate([np.concatenate(
  [t[1:-1, 1:-1] for _, t, _ in r], 1) for r in grid], 0)

sea_monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
sea_p = np.array([[c == '#' for c in row] for row in sea_monster.split('\n')])
for pt in get_transformations(puzzle):
  pattern_match = np.zeros_like(pt)
  any_match = False
  for i in range(puzzle.shape[0]-sea_p.shape[0]+1):
    for j in range(puzzle.shape[1]-sea_p.shape[1]+1):
      match = np.all(pt[i:i+sea_p.shape[0], j:j+sea_p.shape[1]][sea_p])
      if match:
        any_match = True
        pattern_match[i:i+sea_p.shape[0], j:j+sea_p.shape[1]][sea_p] = True
        
  if any_match:
    print((pt & ~pattern_match).sum())
    break