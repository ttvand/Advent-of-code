import numpy as np


data = np.array([19241437, 17346587])
# data = np.array([5764801, 17807724])


loop_sizes = np.zeros_like(data)
step = 1
val = 1
while (loop_sizes > 0).sum() == 0:
  val *= 7
  val = np.mod(val, 20201227)
  new_ids = (loop_sizes == 0) & (val == data)
  loop_sizes[new_ids] = step
  step += 1

loop_id = np.where(loop_sizes > 0)[0][0]
loop_size = loop_sizes[loop_id]
mult_fac = data[1-loop_id]
val = 1
for _ in range(loop_size):
  val = np.mod(val*mult_fac, 20201227)
  
print(val)