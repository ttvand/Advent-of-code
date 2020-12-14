import copy
input_validation = True

filename = 'input04.txt'
with open(filename) as f:
  data = [s.strip() for s in f.readlines()]
data = [''] + data + ['']
num_data_rows = len(data)
  
fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
req_passport = {k: None for k in fields}

person_fields = {}
valid_count = 0
for i in range(num_data_rows):
  if data[i] == '':
    if i > 0:
      valid = True
      for k in fields:
        if person_fields[k] is None and k != 'cid':
          valid = False
          break
      if valid and input_validation:
        byr = person_fields['byr']
        valid_byr = len(byr) == 4 and int(byr) >= 1920 and int(byr) <= 2002
        
        iyr = person_fields['iyr']
        valid_iyr = len(byr) == 4 and int(iyr) >= 2010 and int(iyr) <= 2020
        
        eyr = person_fields['eyr']
        valid_eyr = len(eyr) == 4 and int(eyr) >= 2020 and int(eyr) <= 2030
        
        hgt = person_fields['hgt']
        valid_hgt = False
        if len(hgt) > 3:
          if hgt[-2:] == 'cm' and len(hgt) == 5:
            valid_hgt = int(hgt[:-2]) >= 150 and int(hgt[:-2]) <= 193
          elif hgt[-2:] == 'in' and len(hgt) == 4:
            valid_hgt = int(hgt[:-2]) >= 59 and int(hgt[:-2]) <= 76
            
        hcl = person_fields['hcl']
        valid_hcl = hcl[0] == '#' and len(hcl) == 7
        if valid_hcl:
          for j in range(1, 7):
            c = hcl[j]
            valid_hcl = valid_hcl and c in '0123456789abcdef'
        
        ecl = person_fields['ecl']
        valid_ecl = ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        
        pid = person_fields['pid']
        valid_pid = len(pid) == 9
        if valid_pid:
          for j in range(9):
            pid[j] in '0123456789'
        
        valid = valid and valid_byr and valid_iyr and valid_eyr and (
          valid_hgt) and valid_hcl and valid_ecl and valid_pid
        
      valid_count += int(valid)
    person_fields = copy.copy(req_passport)
  else:
    parts = data[i].split(' ')
    for p in parts:
      sub_parts = p.split(":")
      person_fields[sub_parts[0]] = sub_parts[1]
  
print(valid_count)