import numpy as np
from scipy.signal import convolve2d
from utils import VM

filename = 'input17.txt'
with open(filename) as f: rawProgram = "".join(
    [s.strip() for s in f.readlines()])
memory = [int(i) for i in rawProgram.split(",")]

vm = VM(memory)
#vm.run(p)
#vm.output

while not vm.halted:
  vm.run(0) # The input doesn't matter

chars = [chr(o) for o in vm.output]
newline_pos = np.array(chars) == "\n"
num_cols = np.where(newline_pos)[0][0]
layout = np.reshape(np.array(chars)[~newline_pos], [-1, num_cols])
num_rows = layout.shape[0]

intersection_filter = np.array([[0, 1,  0], [1, 1, 1], [0, 1, 0]])
intersections = convolve2d(layout == '#', intersection_filter, boundary='symm',
                           mode='same') == 5
left_dist = np.tile(np.expand_dims(np.arange(num_cols), 0), [num_rows, 1])
top_dist = np.tile(np.expand_dims(np.arange(num_rows), 1), [1, num_cols])

print("Part1: {}".format((intersections*left_dist*top_dist).sum()))


##########
# Part 2 #
##########

# Determine the path that is to be followed
current = [2, 44]
end_pos = [26, 34]
direction = (0, -1)
left_dirs = {(0, -1): (1, 0), (0, 1): (-1, 0), (1, 0): (0, 1), (-1, 0): (0, -1)}
actions = ["L"]
step_counter = 0

while True:
  next_ = [current[0] + direction[0], current[1] + direction[1]]
#  print(next_)
#  import pdb; pdb.set_trace()
  
  if next_[0] < 0 or next_[0]>= num_rows or (
      next_[1] < 0 or next_[1] >= num_cols) or (
          layout[next_[0], next_[1]] == '.'):
    actions.append(step_counter)
    step_counter = 0
    
    # Check if we have reached the end
    if current[0] == end_pos[0] and current[1] == end_pos[1]:
      break
    
    # Turn the robot to stay on the scaffold and update the direction
    left_dir = left_dirs[direction]
    right_dir = (-left_dir[0], -left_dir[1])
    left_pos = [current[0] + left_dir[0], current[1] + left_dir[1]]
    turn_left = left_pos[0] >= 0 and left_pos[0] < num_rows and (
          left_pos[1] >= 0 and left_pos[1] < num_cols) and (
              layout[left_pos[0], left_pos[1]] == '#')
    actions.append("L" if turn_left else "R")
    direction = left_dir if turn_left else right_dir
    
  else:
    step_counter += 1
    current = next_
    
# Eyeball repeating patterns in the path
all_actions = np.reshape(np.array(actions), [-1, 2])
patterns = {'A': [0, 3], 'B': [3, 7], 'C': [10, 14]}
main_routine = ['A', 'B', 'A', 'C', 'B', 'A', 'C']

# Wake the vacuum robot up
memory2 = memory.copy()
memory2[0] = 2
vm2 = VM(memory2)
inputs = []

# Supply main routine instructions
for i, routine in enumerate(main_routine):
  if i > 0:
    inputs.append(ord(','))
  inputs.append(ord(routine))
inputs.append(ord('\n'))
  

# Supply movement functions
unique_instructions = np.unique(np.array(main_routine))
for instr in unique_instructions:
  pattern = patterns[instr]
  num_steps = pattern[1] - pattern[0]
  for i in range(num_steps):
    if i > 0:
      inputs.append(ord(','))
    action_row = pattern[0] + i
    inputs.append(ord(all_actions[action_row, 0]))
    inputs.append(ord(','))
    for j in range(len(all_actions[action_row, 1])):
      inputs.append(ord(all_actions[action_row, 1][j]))
  inputs.append(ord('\n'))

# Supply continuous video feed instruction
inputs.append(ord('n'))
inputs.append(ord('\n'))

vm2.run(inputs)

print("Part 2: {}".format(vm2.output[-1]))





