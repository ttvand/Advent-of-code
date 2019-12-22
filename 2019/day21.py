import numpy as np
from random import sample 
import string
from utils import VM

filename = 'input21.txt'
with open(filename) as f: rawProgram = "".join(
    [s.strip() for s in f.readlines()])
memory = [int(i) for i in rawProgram.split(",")]

def create_springscript(rules, part1):
  rules.append("WALK" if part1 else "RUN")
  return [ord(x) for x in ("\n".join(rules) + "\n")]
  
#def part1_strategy():
#  strategy = []
#  
#  strategy.append("OR A T")
#  strategy.append("AND B T")
#  strategy.append("AND C T")
#  strategy.append("NOT T T")
#  strategy.append("OR D J")
#  strategy.append("AND T J")
#  
#  return strategy

def random_strategy(num_registers, max_instructions, use_all_instructions):
  strategy = []
  
  valid_instructions = ['AND', 'OR', 'NOT']
  second_chars = ['T', 'J']
  first_chars = list(string.ascii_uppercase[:num_registers]) + second_chars
  
  for i in range(max_instructions):
    sampled_instruction = sample(valid_instructions, 1)[0]
    first_char = sample(first_chars, 1)[0]
    second_char = sample(second_chars, 1)[0]
    if i > 5 and sampled_instruction == 'NOT':
       first_char = sample(second_chars, 1)[0]
    strategy.append("{} {} {}".format(
        sampled_instruction, first_char, second_char))
    
    if not use_all_instructions:
      exit_prob = 1/(max_instructions-i-1)
      if np.random.uniform() < exit_prob:
        break
  
  strategy[-1] = strategy[-1][:-3] + 'T J'
    
  return strategy

def eval_strategy(strategy, req_states):
  for s in strategy:
    parts = s.split(' ')
    if parts[0] == 'NOT':
      req_states[parts[2]] = not req_states[parts[1]]
    elif parts[0] == 'OR':
      req_states[parts[2]] = req_states[parts[1]] or req_states[parts[2]]
    elif parts[0] == 'AND':
      req_states[parts[2]] = req_states[parts[1]] and req_states[parts[2]]
    else:
      raise ValueError('Invalid command')
  
  return req_states['J']

def meets_requirements(strategy, requirements, num_registers,
                       num_other_samples=50):
  
  states = {'T': False, 'J': False}
  registers = list(string.ascii_uppercase[:num_registers])
  
  for _ in range(num_other_samples):
    for i in range(num_registers):
      states[registers[i]] = sample([False, True], 1)[0]
    for req_inputs, req_result in requirements:
      req_states = states.copy()
      for req_input, req_state in req_inputs:
        req_states[req_input] = req_state
      if eval_strategy(strategy, req_states) != req_result:
        return False
      
  return True

def random_requirements_strategy(requirements, num_registers, max_instructions,
                                 use_all_instructions):
  for i in range(int(1e8)):
    print(i)
    strategy = random_strategy(
        num_registers=num_registers,
        max_instructions=max_instructions,
        use_all_instructions=use_all_instructions,
        )
    
    if meets_requirements(strategy, requirements, num_registers):
      break
  return strategy
  
#requirements = [
#    ([('A', False), ('B', False), ('C', False), ('D', True)], True),
#    ([('D', False)], False),
#    ([('A', False), ('B', True), ('C', True), ('D', True)], True),
#    ([('A', True), ('B', False), ('D', True)], True),
#    ([('A', True), ('B', True), ('C', True), ('D', True)], False),
#    
##    ([('A', True), ('B', True), ('C', True), ('D', True)], False),
##    ([('E', False), ('H', False)], False),
##    ([('A', False), ('B', True), ('C', True), ('D', True), ('E', True),
##      ('F', True), ('G', True)], True)
#    ]
#attempt_counter = 0
#while True:
#  attempt_counter += 1
#  vm = VM(memory)
#  strat = random_requirements_strategy(requirements, 4, 15, False)
#  vm_input = create_springscript(strat, part1=True)
#  vm.run(vm_input)
#  try:
#    feedback = ''.join(chr(i) for i in vm.output)
#  except:
#    print("Part 1: {}".format(vm.output[-1])) 
#    break
  

requirements = [
    ([('A', False), ('B', False), ('C', False), ('D', True)], True),
    ([('D', False)], False),
    ([('A', False), ('B', True), ('C', True), ('D', True)], True),
    ([('A', True), ('B', False), ('D', True)], True),
    ([('A', True), ('B', True), ('C', True), ('D', True)], False),
    
    ([('C', False), ('D', True), ('E', False), ('F', False)], True),
    ([('A', True), ('B', True), ('C', False), ('D', True), ('E', False),
      ('F', True), ('G', False), ('H', False)], False),
#    ([('E', False), ('H', False)], False),
#    ([('A', False), ('B', True), ('C', True), ('D', True), ('E', True),
#      ('F', True), ('G', True)], True)
    ]
while True:
  vm = VM(memory)
  strat, attempt_counter = random_requirements_strategy(
      requirements, 9, 15, True)
  vm_input = create_springscript(strat, part1=False)
  vm.run(vm_input)
  try:
    feedback = ''.join(chr(i) for i in vm.output)
    print(meets_requirements(strat[:-1], requirements, 9))
  except:
    print("Part 2: {} after {} iterations".format(vm.output[-1]),
          attempt_counter) 
    break








