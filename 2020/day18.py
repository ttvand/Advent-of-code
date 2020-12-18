import numpy as np


filename = 'input18.txt'

with open(filename) as f:
  data = [d.strip() for d in f.readlines()]
  
def resolve(expr, left_add=0, left_mult=None):
  # Parse part 1
  if expr[0] == '(':
    # Find the position of the closing parenthesis
    open_count = 1
    pos = 1
    while open_count > 0:
      if expr[pos] == '(':
        open_count += 1
      elif  expr[pos] == ')':
        open_count -= 1
      pos += 1
    
    first = resolve(expr[1:pos-1], 0)
    pos -= 1
  else:
    first = int(expr[0])
    pos = 0
    
  # Perform the operator compression
  if left_mult is None:
    compression = left_add + first
  else:
    compression = left_mult * first
    
  # Parse the operator (if any)
  if len(expr) > pos + 1:
    op = expr[pos + 2]
    if op == '*':
      return resolve(expr[pos+4:], left_add=None, left_mult=compression)
    else:
      return resolve(expr[pos+4:], left_add=compression, left_mult=None)
  else:
    return compression
  
sums = np.array([resolve(d, 0) for d in data])
print(sums.sum())

###############################################################################

def add_first(expr):
  processed_pos = []
  while True:
    add_pos = [i for i, c in enumerate(expr) if c == '+']
    add_par_pos = [p for p in add_pos if (
      expr[p-2] != '(' and not p in processed_pos and not (
        len(processed_pos) > 0 and p < processed_pos[-1]))]
    if len(add_par_pos) == 0:
      break
    pos = add_par_pos[0]
    processed_pos.append(pos+1)
    if expr[pos-2] == ')':
      close_count = 1
      start_pos = pos-3
      while close_count > 0:
        if expr[start_pos] == '(':
          close_count -= 1
        elif expr[start_pos] == ')':
          close_count += 1
        start_pos -= 1
      start_pos += 1
    else:
      start_pos = pos-2
      
    if expr[pos+2] == '(':
      open_count = 1
      end_pos = pos+3
      while open_count > 0:
        if expr[end_pos] == '(':
          open_count += 1
        elif expr[end_pos] == ')':
          open_count -= 1
        end_pos += 1
    else:
      end_pos = pos + 3
    expr = expr[:start_pos] + '(' + expr[start_pos:end_pos] + ')' + expr[
      end_pos:]
  return expr

# Add parentheses to make sure addition takes precedence over multiplication
data_add_first = [add_first(d) for d in data]
sums = np.array([resolve(d, 0) for d in data_add_first])
print(sums.sum())