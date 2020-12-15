N = [2020, int(3e7)][1]
puzzle_input = [12, 20, 0, 6, 1, 17, 7]
# puzzle_input = [0, 3, 6]

memory = {ip: id_ for id_, ip in enumerate(puzzle_input[:-1])}
last = puzzle_input[-1]
step = len(memory)
while step < N-1:
  if last in memory:
    mem_cp = memory[last]
    memory[last] = step
    last = step - mem_cp
  else:
    memory[last] = step
    last = 0
  
  step += 1
  
print(last)