import numpy as np
from random import sample 
import string
from utils import VM

filename = 'input23.txt'
with open(filename) as f: rawProgram = "".join(
    [s.strip() for s in f.readlines()])
memory = [int(i) for i in rawProgram.split(",")]

num_machines = 50
vms = []
for i in range(num_machines):
  vm = VM(memory)
  vm.run([i])
  vms.append(vm)
  
vm_queues = [[] for i in range(num_machines)]
step = 0
while True:
#  import pdb; pdb.set_trace()
  print(step, np.array([len(m) for m in vm_queues]).sum())
  step += 1  
  
  if step == 10:
    break
  
  # Update inputs
  for i in range(num_machines):
    if vm_queues[i]:
      input_instr = [vm_queues[i].pop()]
    else:
      input_instr = [-1]
    vms[i].run(input_instr, return_interval=3, return_after_read=True)
    
  # Update output instructions
  for i in range(num_machines):
    m_outputs = vms[i].last_outputs_block
    if vms[i].last_outputs_block:
#      if step > 0:
#        import pdb; pdb.set_trace()
#        x=1
      if m_outputs[0] > 49:
        import pdb; pdb.set_trace()
        x=1
      vm_queues[m_outputs[0]].extend(m_outputs[1:3])
