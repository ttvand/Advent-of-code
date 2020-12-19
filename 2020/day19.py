import numpy as np


filename = 'input19.txt'
# filename = 'input19_2.txt'

with open(filename) as f:
  data = [d.strip() for d in f.readlines()]
  
# Parse the inputs
empty_line = [i for i, d in enumerate(data) if len(d) == 0][0]
rules = {int(data[i].split(': ')[0]): data[i].replace('"', '').split(
  ': ')[1].split(' | ') for i in range(empty_line)}
messages = data[empty_line+1:]

# Compute the rule lengths
rule_lengths = {k: int(1) if v in [['a'], ['b']] else 0 for k, v in rules.items()}
def add_rule_lengths(rule_k, rule_lengths):
  if rule_lengths[rule_k] > 0:
    return rule_lengths[rule_k]
  
  rule = rules[rule_k]
  num_parts = len(rule)
  lengths = np.zeros(num_parts, dtype=np.int)
  for i in range(num_parts):
    lengths[i] = np.array([add_rule_lengths(int(c), rule_lengths) for c in (
      rule[i].split(' '))]).sum()
  
  if lengths.size > 1:
    if not np.all((lengths) == lengths[0]):
      import pdb; pdb.set_trace()
    
  rule_lengths[rule_k] = lengths[0]
  return lengths[0]
  
for k in rule_lengths:
  add_rule_lengths(k, rule_lengths)

# Part 1
def matches(message, rule_k, memory, part_2=False):
  if not message:
    return False
  
  if (rule_k, message) in memory:
    return memory[(rule_k, message)]
  
  if len(message) == 1:
    val = message in [r if r in ['a', 'b'] else rules[int(r)][0] for r in rules[rule_k]]
    memory[(rule_k, message)] = val
    return memory[(rule_k, message)]
  
  for sr in rules[rule_k]:
    start_pos = 0
    is_sub_match = True
    for c in sr.split(' '):
      rule_len = rule_lengths[int(c)]
      if not matches(message[start_pos:(start_pos+rule_len)], int(c), memory):
        is_sub_match = False
        break
      else:
        start_pos += rule_len
    
    if is_sub_match and start_pos == len(message):
      memory[(rule_k, message)] = True
      return memory[(rule_k, message)]
  
  memory[(rule_k, message)] = False
  return memory[(rule_k, message)]
  
memory = {}
valid_counts = np.array([int(matches(m, 0, memory)) for m in messages])
print(valid_counts.sum())

# Part 2: match 1+ 42's and 1+42-31 sequences
part_2_matches = np.zeros(len(messages))
for i, m in enumerate(messages):
  pos = 0
  num_lead_42 = 0
  num_trail_31 = 0
  exit_part_1 = False
  exit_part_2 = False
  while not exit_part_1 and pos < len(m):
    if matches(m[pos:pos+rule_lengths[42]], 42, memory):
      num_lead_42 += 1
    else:
      pos -= rule_lengths[42]
      exit_part_1 = True
    pos += rule_lengths[42]
    
  while not exit_part_2 and pos < len(m):
    if matches(m[pos:pos+rule_lengths[31]], 31, memory):
      num_trail_31 += 1
    else:
      exit_part_2 = True
    pos += rule_lengths[31]
    
  if pos == len(m):
    part_2_matches[i] = int(num_lead_42 > 0 and num_trail_31 > 0 and (
      num_lead_42 > num_trail_31) and (num_lead_42+num_trail_31)==pos//8)
  else:
    part_2_matches[i] = False
    
print(part_2_matches.sum())