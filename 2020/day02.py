import numpy as np

filename = 'input02.txt'
with open(filename) as f:
  data = [s.strip() for s in f.readlines()]
  
policies = []
passwords = []
for d in data:
  spl = d.split(': ')
  passwords.append(spl[1])
  v_parts = spl[0].split(' ')
  policies.append(tuple([int(e) for e in v_parts[0].split('-')] + [
    ord(v_parts[1]) - ord('a')]))
  
num_passwords = len(passwords)
char_counts = np.zeros((num_passwords, 26))

for i, p in enumerate(passwords):
  for l in p:
    letter_id = ord(l) - ord('a')
    char_counts[i, letter_id] += 1

valid_passwords = np.zeros((num_passwords, num_passwords), dtype=np.bool)
for i, (min_p, max_p, l_id) in enumerate(policies):
  valid_passwords[i] = (char_counts[:, l_id] >= min_p) & (
    char_counts[:, l_id] <= max_p)
  
print((valid_passwords*np.eye(num_passwords)).sum())

valid_count = 0
for i, p in enumerate(passwords):
  valid_count += int((
    ord(passwords[i][policies[i][0]-1]) == policies[i][2] + ord('a')) != (
    ord(passwords[i][policies[i][1]-1]) == policies[i][2] + ord('a')))
print(valid_count)