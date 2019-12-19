from utils import VM

filename = 'input15.txt'
with open(filename) as f: rawProgram = "".join(
    [s.strip() for s in f.readlines()])
memory = [int(i) for i in rawProgram.split(",")]

moves = [None, (0, 1), (0, -1), (-1, 0), (1, 0)]

vm = VM(memory)
#vm.run(p)
#vm.output

start_pos = (0, 0)
explored_open = set([start_pos])
queue = [(start_pos, [])] # Current pos, length, path to current
oxygen_pos = None

while queue:
  # Visit all states
  (x_pos, y_pos), path = queue.pop()
  
  # Follow the path to the start position
  for step in path:
    vm.run(step)
    assert(vm.output[-1] == 1)
      
  for command in range(1, 5):
    new_path = path + [command]
    vm.run(command)
    output = vm.output[-1]
    new_pos = (x_pos + moves[command][0], y_pos + moves[command][1])
    
    if output == 1:
      if not new_pos in explored_open:
        queue.append((new_pos, new_path))
        explored_open.add(new_pos)
      
    if output == 2:
      oxygen_pos = new_pos 
      
    if output > 0:
      # Undo the command
      undo_command = 1 + 2*((command - 1) // 2) + (command % 2 != 0)
      vm.run(undo_command)
      assert(vm.output[-1] == 1)
      
  for step in path[::-1]:
    undo_step = 1 + 2*((step  - 1) // 2) + (step  % 2 != 0)
    vm.run(undo_step)
    assert(vm.output[-1] == 1)
    
flooded = set([start_pos])
flood_boundary = set([start_pos])
steps = 0
while flood_boundary:
  new_boundary = set()
  for el in flood_boundary:
    for i in range(1, 5):
      new_el = (el[0] + moves[i][0], el[1] + moves[i][1])
      if new_el == oxygen_pos:
        print("Part 1: {}".format(steps + 1))
      if new_el in explored_open and not new_el in flooded:
        new_boundary.add(new_el)
        flooded.add(new_el)
  
  flood_boundary = new_boundary
  steps += 1
  
  if oxygen_pos in flood_boundary:
    break
  
  
flooded = set([oxygen_pos])
flood_boundary = set([oxygen_pos])
steps = 0
while flood_boundary:
  new_boundary = set()
  for el in flood_boundary:
    for i in range(1, 5):
      new_el = (el[0] + moves[i][0], el[1] + moves[i][1])
      if new_el in explored_open and not new_el in flooded:
        new_boundary.add(new_el)
        flooded.add(new_el)
  
  flood_boundary = new_boundary
  steps += 1
  
  if oxygen_pos in flood_boundary:
    break
print("Part 2: {}".format(steps-1))
  
    
    




    
    
    
    
    
  
  