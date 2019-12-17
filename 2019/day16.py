import numpy as np

filename = 'input16.txt'
with open(filename) as f:
  input_vals = "".join([s.strip() for s in f.readlines()])

#input_vals = '12345678'
base_pattern = np.array([0, 1, 0, -1])

def get_mult_m(base_pattern, num_digits):
  mult_m = np.zeros((num_digits, num_digits))
  pattern_length = base_pattern.size
  for i in range(num_digits):
    num_repeats = int(np.ceil((num_digits+1) / ((i+1)*pattern_length)))
    rep_pat = np.tile(np.repeat(base_pattern, i+1), num_repeats)
    mult_m[i] = rep_pat[1:(num_digits+1)]
    
  return mult_m

def get_fft(input_vals, steps, base_pattern):
  digits = np.array(list(input_vals), dtype=int)
  num_digits = digits.size
  mult_m = get_mult_m(base_pattern, num_digits)
  for i in range(steps):
    digits_m = np.tile(np.expand_dims(digits, 0), [num_digits, 1])
    digits = np.mod(np.abs((mult_m*digits_m).sum(1)), 10)
    
  return digits.astype(np.int)

def get_fft_fixed_base(input_string):
  offset = int(input_string[:7], 10)
  input_list = np.array(list(map(int, input_string)) * 10000)
  input_length = len(input_list)
  
  for i in range(100):
    revsums = np.flip(np.cumsum(np.flip(input_list[offset:input_length])))
    input_list[offset:input_length] = np.mod(np.abs(revsums), 10).astype(np.int)
#    partial_sum = input_list[offset:input_length].sum()
#    for j in range(offset, input_length):
#      t = partial_sum
#      partial_sum -= input_list[j]
#      input_list[j] = t % 10 if t > 0 else -t % 10
  
  return input_list[offset: offset+8]
    
res_1 = get_fft(input_vals, 100, base_pattern)
print('Part 1: {}'.format(res_1[:8]))

res_2 = get_fft_fixed_base(input_vals)
print('Part 1: {}'.format(res_2))