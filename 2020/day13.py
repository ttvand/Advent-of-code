import numpy as np

filename = 'input13.txt'
# filename = 'input13_2.txt'

with open(filename) as f:
  data = [s for s in f.readlines()]

start = int(data[0])
bus_ids = np.array([int(x) for x in data[1].split(',') if x != 'x'])
bus_delays = np.array([i for i, x in enumerate(data[1].split(',')) if x != 'x'])
start_times = np.array([np.round(np.ceil(start/i)*i) for i in bus_ids]).astype(
  np.int)
earliest_id = np.argmin(start_times)
print(bus_ids[earliest_id]*(start_times[earliest_id]-start))

####################################################################

def chinese_remainder(n, a):
  s = 0
  prod = np.prod(n)
  for n_i, a_i in zip(n, a):
    p = prod // n_i
    s += a_i * mul_inv(p, n_i) * p
  return s % prod
 
def mul_inv(a, b):
  b0 = b
  x0, x1 = 0, 1
  if b == 1:
    return 1
  while a > 1:
    q = a // b
    a, b = b, a % b
    x0, x1 = x1 - q * x0, x0
  if x1 < 0:
    x1 += b0
  return x1

a = [-bus_delays[i] % bus_ids[i] for i in range(bus_ids.size)]
print(chinese_remainder(bus_ids.tolist(), a))