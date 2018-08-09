import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('file_pattern', type=str,
                    help='The pattern for the dump files (e.g. "dump_*.liggghts")')
parser.add_argument('num_atom_types', type=int,
                    help='The number of different atom/particle types')
args = parser.parse_args()

files = os.listdir('.')
sim_files = []
for file in files:
    s = args.file_pattern.split('*')
    if file.startswith(s[0]) and file.endswith(s[1]):
        sim_files.append(file)
        
tally = [0]*args.num_atom_types

for file in sim_files:
    with open(file, 'r') as f:
        file_list = []
        sub_file_lines = []
        s = args.file_pattern.split('*')
        file_timestep = int(file[len(s[0]):-len(s[1])])
        lines = f.readlines()
        
        for i in range(args.num_atom_types):
            file_list.append(open(str(i+1) + '_' + str(file_timestep) + '.liggghts', 'w'))
            sub_file_lines.append(lines[:9])
        
        for line in lines[9:]:
            split_line = line.split(' ')
            atom_type = int(split_line[1])-1
            tally[atom_type] += 1
            sub_file_lines[atom_type].append(line)
        
        for sub_file in range(len(sub_file_lines)):
            sub_file_lines[sub_file][3] = str(tally[sub_file]) + '\n'
            file_list[sub_file].writelines(sub_file_lines[sub_file])
        for file in file_list:
            file.close()
