from math import gcd as bltin_gcd
import gmpy2
import numpy as np

debug = False
filename = 'input22_2.txt' if debug else 'input22.txt'
with open(filename) as f: actions = [s.strip() for s in f.readlines()]

# Parse the input
parsed = []
num_actions = len(actions)
commands = [
    ("deal with increment", "increment", True),
    ("cut", "cut", True),
    ("deal into new stack", "new", False),
    ]
for i, a in enumerate(actions):
  for command, short_command, has_arg in commands:
    command_len = len(command)
    if len(a) >= command_len and a[:command_len] == command:
      command_val = int(a[command_len+1:]) if has_arg else None
      parsed.append((short_command, command_val))
      
def final_from_initial(parsed, deck_size, initial_pos):
  pos = initial_pos
  for a, a_arg in parsed:
    if a == "increment":
#      assert bltin_gcd(a_arg, deck_size) == 1
      pos = pos*a_arg % deck_size
    elif a == "cut":
      pos = (pos - a_arg) % deck_size
    elif a == "new":
      pos = deck_size - 1 - pos
    else:
      raise ValueError("Invalid action {}". format(a))
      
  return pos

def initial_from_final(parsed, deck_size, final_pos):
  pos = final_pos
  for a, a_arg in parsed[::-1]:
    if a == "increment":
#      round_increment = (deck_size - a_arg * (deck_size//a_arg))
      round_increment = (a_arg * (1 + deck_size//a_arg) - deck_size)
      target_increment = pos % a_arg
      # SOLVE X*round_increment mod a_arg = target_increment
      x = (int(gmpy2.invert(round_increment, a_arg)) * target_increment) % a_arg
      round_steps = pos // a_arg
      prev_rounds_steps = int(np.ceil(deck_size/a_arg*x))
      pos = round_steps + prev_rounds_steps
    elif a == "cut":
      pos = (pos + a_arg) % deck_size
    elif a == "new":
      pos = deck_size - 1 - pos
    else:
      raise ValueError("Invalid action {}". format(a))
      
  return pos

def part2(parsed, deck_size, final_pos):
  # Sum the cuts and new's
  num_news = np.array([p[0] == "new" for p in parsed]).sum()
  cut_sum = np.array([p[1] for p in parsed if p[0] == "cut"]).sum()
  
  initial_from_final(parsed, deck_size, final_pos)
  
  # Look for cycles
  original_final_pos = final_pos
  positions = [final_pos]
  for i in range(int(1e6)):
    final_pos = initial_from_final(parsed, deck_size, final_pos)
    positions.append(final_pos)
    
    if final_pos == original_final_pos:
      import pdb; pdb.set_trace()
      x=1
      
  import pdb; pdb.set_trace()
  x=1
  
def my_mod_matmul(m1, m2, mod):
  out_rows = m1.shape[0]
  num_ops = m1.shape[1]
  assert(num_ops == m2.shape[0])
  out_cols = m2.shape[1]
  output_m = np.zeros((out_rows, out_cols)).astype(np.int64)
  
  for i in range(out_rows):
    for j in range(out_cols):
      acc = 0
      for k in range(num_ops):
        acc += gmpy2.mpz(m1[i, k]) * gmpy2.mpz(m2[k, j])
      output_m[i, j] = int(gmpy2.f_mod(acc, mod))
  
  return output_m
  
def part2_take2(parsed, deck_size, num_shuffles, final_pos):
  # Determine how the parsed transforms modify the offsets and increments
  start_id = 0
  step_size = 1
  for a, a_arg in parsed:
    if a == "increment":
      step_size *= int(gmpy2.invert(a_arg, deck_size))
    elif a == "cut":
      start_id += a_arg*step_size
    elif a == "new":
      step_size *= -1
      start_id += step_size
    else:
      raise ValueError("Invalid action {}". format(a))
      
    step_size = step_size % deck_size
    start_id = start_id % deck_size
      
  # Define the update matrix of step_size and start_id
  update_m = np.array([[step_size, 0], [start_id, 1]], dtype=np.int64)
  original_update_m = update_m
  
  # Elevate the matrix to the requested number of shuffles
  shuffle_boolean = list("{0:064b}".format(num_shuffles))
  shuffle_rep = np.array([[1], [0]])
  for b in shuffle_boolean[::-1]:
    if int(b):
      shuffle_rep = my_mod_matmul(update_m, shuffle_rep, deck_size)
    update_m = my_mod_matmul(update_m, update_m, deck_size)
    
  return np.mod(shuffle_rep[1][0] + 2020*shuffle_rep[0][0], deck_size)
      
if debug:
  print("part 1: {}".format(final_from_initial(parsed, 10, 3)))
  print("part 2: {}".format(initial_from_final(parsed, 10, 0)))
else:
  print("part 1: {}".format(final_from_initial(parsed, 10007, 2019)))
  print("part 2: {}".format(part2_take2(parsed, 119315717514047,
        101741582076661, 2020)))
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  