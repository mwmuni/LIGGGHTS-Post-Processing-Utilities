import argparse
import os
import csv
import multiprocessing as mp
import threading
import _thread
import time
import itertools

tally_tracker = []

class myThread (threading.Thread):
   def __init__(self, threadID, file, num_atoms, s):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.file = file
      self.num_atoms = num_atoms
      self.s = s
   def run(self):
      process(self.file, self.num_atoms, self.s)

def process(file, num_atoms, s):
    with open(file, 'r') as f:
        file_timestep = int(file[len(s[0]):-len(s[1])])
        lines = f.readlines()
        tally = [0]*num_atoms
        
        for line in lines[9:]:
            split_line = line.split(' ')
            atom_type = int(split_line[1])-1
            tally[atom_type] += 1

        global tally_tracker
        tally_tracker.append((file_timestep, *tally))

if __name__ == '__main__':
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
    
    s = args.file_pattern.split('*')

    x = itertools.count()
    p = []
    for fl in sim_files:
        p.append(myThread(next(x), fl, 2, s))

    step=24
    for i in range(step, len(sim_files), step):
        print('Reading [' + str(i-step) + ':' + str(i-1) + '] of ' + str(len(sim_files)))
        for j in range(i-step, i):
            p[j].start()
        for proc in p[i-step:i]:
            p[j].join()
        while not threading.activeCount() == 2:
            pass

    print('Reading [' + str(len(p) - (len(p)%step)) + ':' + str(len(p)) + '] of ' + str(len(p)))
    for proc in p[len(p) - (len(p)%step):len(p)+1]:
        proc.start()
    for proc in p[len(p) - (len(p)%step):len(p)+1]:
        proc.join()

    csv_file = csv.writer(open(s[0]+'.csv', 'w', newline=''))

    temp = ['timestep']
    temp.extend([('particle_'+str(i+1)) for i in range(args.num_atom_types)])

    csv_file.writerow(temp)
    csv_file.writerows(sorted(tally_tracker, key=lambda x: x[0]))
