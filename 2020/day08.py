import copy
import numpy as np

filename = '../../Downloads/input08.txt'
with open(filename) as f:
  data = [s for s in f.readlines()]

ops = []
for d in data:
  op_parts = d.split(' ')
  ops.append((op_parts[0], int(op_parts[1]), False))
  
def execute_modified(ops, modify_row=None):
  if modify_row is not None:
    op, arg, executed = ops[modify_row]
    new_op = {'acc': 'acc', 'jmp': 'nop', 'nop': 'jmp'}[op]
    ops[modify_row] = (new_op, arg, executed)
  acc = 0
  pointer = 0
  while pointer < len(ops) and not ops[pointer][2]:
    ops[pointer] = (ops[pointer][0], ops[pointer][1], True)
    op, arg, _ = ops[pointer]
    if op == 'acc':
      acc += arg
      pointer += 1
    elif op == 'jmp':
      pointer += arg
    elif op == 'nop':
      pointer += 1
  successful = pointer >= len(ops)
  
  return acc, successful
  
results = []
for i in range(len(ops)):
  results.append(execute_modified(copy.copy(ops), modify_row=i))
  
mods = np.array(results)