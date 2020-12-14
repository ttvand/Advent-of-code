import numpy as np


filename = 'input05.txt'
with open(filename) as f:
  data = [s.strip() for s in f.readlines()]

def get_seat_id(seat):
  row_id = int(''.join(['1' if c == 'B' else '0' for c in seat[:7]]), 2)
  col_id = int(''.join(['1' if c == 'R' else '0' for c in seat[7:]]), 2)
  
  return row_id*8+col_id
  
seats_taken = np.zeros(128*8)
for seat in data:
  seats_taken[get_seat_id(seat)] = True
  
print(np.where(seats_taken)[0].max())