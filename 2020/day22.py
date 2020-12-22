import copy
import numpy as np


filename = 'input22.txt'
# filename = 'input22_2.txt'

with open(filename) as f:
  data = [d.strip() for d in f.readlines()]
  
# Extract the inputs
num_cards = (len(data)-3)//2
p1 = [int(d) for d in data[1:1+num_cards]]
p2 = [int(d) for d in data[num_cards+3:num_cards*2+3]]

# Part 1
while len(p1)*len(p2) > 0:
  f, s = p1.pop(0), p2.pop(0)
  
  if f > s:
    p1.append(f)
    p1.append(s)
  else:
    p2.append(s)
    p2.append(f)
    
winner = p1 if len(p1) else p2
print((np.flip(1+np.arange(num_cards*2))*np.array(winner)).sum())

# Part 2
def rec_combat(p1, p2, hist, games):
  state = (tuple(p1), tuple(p2))
  if state in games:
    return games[state], p1, p2
  
  while len(p1)*len(p2) > 0:
    f, s = p1.pop(0), p2.pop(0)
    
    if len(p1) >= f and len(p2) >= s:
      first_winner = rec_combat(copy.copy(p1[:f]), copy.copy(p2[:s]), [],
                                games)[0]
      games[(tuple(p1), tuple(p2))] = first_winner
      if first_winner:
        p1.append(f)
        p1.append(s)
      else:
        p2.append(s)
        p2.append(f)
    else:
      if f > s:
        p1.append(f)
        p1.append(s)
      else:
        p2.append(s)
        p2.append(f)
      
    state = (tuple(p1), tuple(p2))
    if state in hist:
      return True, p1, p2
    hist.append(state)
    
  first_win = len(p1) > 0
  if first_win:
    return True, p1, p2
  else:
    return False, p2, p1
  
p1 = [int(d) for d in data[1:1+num_cards]]
p2 = [int(d) for d in data[num_cards+3:num_cards*2+3]]
winner, pw, pl = rec_combat(p1, p2, [], {})
print((np.flip(1+np.arange(num_cards*2))*np.array(pw)).sum())