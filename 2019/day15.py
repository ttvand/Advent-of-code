import os

class VM:
    def __init__(self, memory):
        self.memory = memory[:]
        self.pc = 0
        self.inputPtr = 0
        self.inputBuffer = []
        self.output = []
        self.base = 0
        self.halted = False

    def __parseMode(self, data, mode, rw):
        if rw.lower() == "read":
            if mode == 0: return self[data]
            elif mode == 1: return data
            elif mode == 2: return self[self.base+data]
        elif rw.lower() == "write":
            if mode == 0: return data
            elif mode == 1: return data
            elif mode == 2: return self.base+data
        else:
            raise Exception("Invalid read/write mode ({}).".format(rw))

    def __getInput(self):
        if self.inputPtr < len(self.inputBuffer):
            self.inputPtr += 1
            return self.inputBuffer[self.inputPtr-1]
        else:
            return None

    def __getitem__(self, pos):
        if pos < 0: raise Exception("Can't acess negative memory address ({}).".format(pos))

        if pos >= len(self.memory):
            self.memory += [0 for _ in range(pos+1-len(self.memory))]
        return self.memory[pos]

    def __setitem__(self, pos, data):
        if pos < 0: raise Exception("Can't acess negative memory address ({}).".format(pos))

        if pos >= len(self.memory):
            self.memory += [0 for _ in range(pos+1-len(self.memory))]
        self.memory[pos] = data

    def run(self, inputValue=None):
        if type(inputValue) is list:
            self.inputBuffer += inputValue
        elif inputValue is not None:
            self.inputBuffer.append(int(inputValue))

        while self.pc < len(self.memory):
            paramAndOpcode = "{:05}".format(self[self.pc])
            opcode = int(paramAndOpcode[-2:])
            modeC, modeB, modeA = [int(i) for i in paramAndOpcode[:3]]

            a, b, c = None, None, None
            if opcode in [4, 9]: # out, arb
                a = self.__parseMode(self[self.pc+1], modeA, "read")
                npc = self.pc+2
            elif opcode in [3]: # in
                a = self.__parseMode(self[self.pc+1], modeA, "write")
                npc = self.pc+2
            elif opcode in [5, 6]: # jit, jif
                a = self.__parseMode(self[self.pc+1], modeA, "read")
                b = self.__parseMode(self[self.pc+2], modeB, "read")
                npc = self.pc+3
            elif opcode in [1, 2, 7, 8]: # add, mul, lt, eq
                a = self.__parseMode(self[self.pc+1], modeA, "read")
                b = self.__parseMode(self[self.pc+2], modeB, "read")
                c = self.__parseMode(self[self.pc+3], modeC, "write")
                npc = self.pc+4

            if opcode == 1: # add
                self[c] = a + b
            elif opcode == 2: # mul
                self[c] = a * b
            elif opcode == 3: # in
                i = self.__getInput()
                if i is not None:
                    self[a] = i
                else:
                    return
            elif opcode == 4: # out
                self.output.append(a)
            elif opcode == 5: # jit
                if a != 0: npc = b
            elif opcode == 6: # jif
                if a == 0: npc = b
            elif opcode == 7: # lt
                self[c] = int(a < b)
            elif opcode == 8: # eq
                self[c] = int(a == b)
            elif opcode == 9: # arb
                self.base += a
            elif opcode == 99:
                break

            self.pc = npc

        self.halted = True
        return

###############################

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
  
    
    




    
    
    
    
    
  
  