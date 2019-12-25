import itertools
import numpy as np
from utils import VM

filename = 'input25.txt'
with open(filename) as f: rawProgram = "".join(
    [s.strip() for s in f.readlines()])
memory = [int(i) for i in rawProgram.split(",")]

def make_command(command):
  return [ord(x) for x in list(command) + ["\n"]]

def get_valid_moves(state):
  feedback = ''.join(chr(i) for i in state)
  print(feedback)
  
def get_state(state):
  np_state = np.array(state)
  equal_ids = np.where(np_state == 61)[0]
  colon_ids = np.where(np_state == 58)[0]
  colon_ids = colon_ids[colon_ids > 25]
  dash_ids = np.where(np_state == 45)[0]
  dash_ids = dash_ids[dash_ids>colon_ids[0]]
  newline_ids = np.where(np_state == 10)[0]
  feedback = ''.join(chr(i) for i in state)
  print(feedback)
  
  # Extract the name of the room
  room_name = feedback[(equal_ids[1]+2):(equal_ids[2]-1)]
  
  # Extract valid directions
  dirs = []
  dash_id = 0
  while True:
    next_newline_pos = newline_ids[newline_ids>dash_ids[dash_id]][0]
    dir_ = feedback[(dash_ids[dash_id]+2):next_newline_pos]
    dirs.append(dir_)
      
    dash_id += 1
    if dash_id == dash_ids.size or ((
        dash_ids[dash_id] - dash_ids[dash_id-1]) > 10):
      break
  
  # Extract items in the room
  items = []
  if colon_ids.size > 1:
#     and not room_name in ["Stables", "Hot Chocolate Fountain"]
    while True:
      next_newline_pos = newline_ids[newline_ids>dash_ids[dash_id]][0]
      item_ = feedback[(dash_ids[dash_id]+2):next_newline_pos]
      items.append(item_)
        
      dash_id += 1
      if dash_id == dash_ids.size:
        break
      
  state = (room_name, dirs, items)
  return state
  
def make_move(vm, command):
  if command is not None:
    com_ascii = make_command(command)
    vm.run(com_ascii)
  
  # Clear output before room id and after first '?'
  equal_ids = np.where(np.array(vm.output) == 61)[0]
  if equal_ids.size:
    vm.output = vm.output[equal_ids[-4]:]
    
#  command_pos = re.search(
#      "Command", ''.join(chr(i) for i in vm.output)).start()
#  vm.output = vm.output[:command_pos]
#  question_ids = np.where(np.array(vm.output) == ord('?'))[0]
#  question_ids = question_ids[question_ids > 100]
#  if question_ids.size > 1:
#    vm.output = vm.output[:question_ids[0]]
    
  next_state = get_state(vm.output)
  
  return vm, next_state

def part1(vm):
  # Wander around, pick up all items you encounter and can carry
  rooms = {}
  have = set()
  vm, _ = make_move(vm, 'inv')
  def traverse(path):
    global vm
    vm, state = make_move(vm, None)
    roomname = state[0]
    if roomname in rooms:
      return
    rooms[roomname] = path

    for it in state[2]:
      if it not in ('escape pod', 'infinite loop', 'giant electromagnet',
                    'photons', 'molten lava'):
        vm, _ = make_move(vm, 'take ' + it)
        have.add(it)

    for direc in state[1]:
      vm, _ = make_move(vm, direc)
      traverse(path + (direc,))
      bw = {
          'north': 'south',
          'south': 'north',
          'east': 'west',
          'west': 'east',
      }
      vm, _ = make_move(vm, bw[direc])
        
  traverse(())
  
  # Navigate to the security checkpoint
  for step in rooms['Security Checkpoint']:
    vm, _ = make_move(vm, step)
    
  # Drop all items
  for it in have:
    vm, _ = make_move(vm, 'drop ' + it)
    
  # Try all item combinations
  for j in range(len(have)):
    considered_sets = list(itertools.combinations(have, j))
    for ss in considered_sets:
      for it in ss:
        vm, _ = make_move(vm, 'take ' + it)
      vm, _ = make_move(vm, 'north')
      o = ''.join(map(chr, vm.output))
      if vm.halted:
        print(o)
        break
      else:
        for it in ss:
          vm, _ = make_move(vm, 'drop ' + it)
  
vm = VM(memory)
part1(vm)