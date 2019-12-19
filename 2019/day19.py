import numpy as np
from utils import VM

filename = 'input19.txt'
with open(filename) as f: rawProgram = "".join(
    [s.strip() for s in f.readlines()])
memory = [int(i) for i in rawProgram.split(",")]

vm = VM(memory)

grid_size = 50
collect_size = 2000
ship_width = 100
start_col = 0
beam_sum = 0
ray_ratio = 1.4
for i in range(collect_size):
  if i == 50:
    print("Part 1: {}".format(beam_sum))
  next_start_col = np.inf
  prev_start_col = start_col
  beam_width = 0
  zero_gap_patience = 2
  for j in range(start_col, collect_size):
    vm.run([i, j])
    int_output = vm.output[-1]
    vm = VM(memory)
    if int_output == 0:
      zero_gap_patience -= 1
      if zero_gap_patience == 0:
        break
    else:
      beam_width += 1
      if j < next_start_col:
        next_start_col = j
  beam_sum += beam_width
  
  print(i, beam_width)
  if beam_width >= ship_width*ray_ratio:
    # Make sure that the height of the biggest group is sufficient
    considered_col = next_start_col + beam_width - ship_width
    coded_pos = considered_col + 10000*i
    height_count = 0
    height_offset = 1
    while True:
      vm.run([i+height_offset, considered_col])
      int_output = vm.output[-1]
      vm = VM(memory)
      if int_output == 0:
        break
      else:
        height_offset = height_offset + 1
    print("Offset: {}".format(height_offset))
    if height_offset == ship_width:
      part2_coded = coded_pos
      break
  
  start_col = next_start_col if np.isfinite(next_start_col) else prev_start_col
  
print("Part 2: {}".format(part2_coded))