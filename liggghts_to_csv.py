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
    #   print ("Starting " + self.file)
      process(self.file, self.num_atoms, self.s)
    #   print ("Exiting " + self.file)

def process(file, num_atoms, s):
    with open(file, 'r') as f:
        # print('accessed')
        file_timestep = int(file[len(s[0]):-len(s[1])])
        lines = f.readlines()
        tally = [0]*num_atoms
        
        for line in lines[9:]:
            split_line = line.split(' ')
            atom_type = int(split_line[1])-1
            tally[atom_type] += 1

        # store((file_timestep, *tally))
        # print('finished processing')
        # atom = None
        # while atom is None:
        #     atom = q.get() if not q.empty() else None
        #     time.sleep(1/100)
        # print('before', tally_tracker)
        global tally_tracker
        tally_tracker.append((file_timestep, *tally))
        # print('after', tally_tracker)
        # q.put(1)
        # tally_tracker.append((file_timestep, *tally))
        # q.put([file_timestep, *tally])

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

    # tally_tracker
    
    s = args.file_pattern.split('*')

    q = mp.Queue()
    q.put(1)

    # p = [_thread.start_new_thread(process, (q,fl,args.num_atom_types, s)) for fl in sim_files]

    x = itertools.count()
    p = []
    for fl in sim_files:
        p.append(myThread(next(x), fl, 2, s))
    # p = [myThread() for fl in sim_files]

    step=24
    for i in range(step, len(sim_files), step):
        print('Reading [' + str(i-step) + ':' + str(i-1) + '] of ' + str(len(sim_files)))
        for j in range(i-step, i):
            p[j].start()
        for proc in p[i-step:i]:
            p[j].join()
        while not threading.activeCount() == 2:
            # print(threading.activeCount())
            # time.sleep(1/10)
            pass

    # step=12
    # for i in range(step, len(sim_files), step):
    #     print('Reading [' + str(i-step) + ':' + str(i-1) + '] of ' + str(len(sim_files)))
    #     for proc in p[i-step:i]:
    #         proc.start()
    #     for proc in p[i-step:i]:
    #         proc.join()
    #     for proc in p[i-step:i]:
    #         proc.terminate()
    #     break
        # exit()
        # while not q.empty():
        #     tally_tracker.append(q.get())

    print('Reading [' + str(len(p) - (len(p)%step)) + ':' + str(len(p)) + '] of ' + str(len(p)))
    for proc in p[len(p) - (len(p)%step):len(p)+1]:
        proc.start()
    for proc in p[len(p) - (len(p)%step):len(p)+1]:
        proc.join()


    # while not q.empty():
    #     tally_tracker.append(q.get())



    # for file in sim_files:
    #     with open(file, 'r') as f:
    #         s = args.file_pattern.split('*')
    #         file_timestep = int(file[len(s[0]):-len(s[1])])
    #         lines = f.readlines()
            
    #         for line in lines[9:]:
    #             split_line = line.split(' ')
    #             atom_type = int(split_line[1])-1
    #             tally[atom_type] += 1

    #         tally_tracker.append([file_timestep, *tally])

    #         for i in range(len(tally)):
    #             tally[i] = 0

    csv_file = csv.writer(open(s[0]+'.csv', 'w', newline=''))

    # print(tally_tracker)
    # print(len(tally_tracker))

    temp = ['timestep']
    temp.extend([('particle_'+str(i+1)) for i in range(args.num_atom_types)])

    csv_file.writerow(temp)
    csv_file.writerows(sorted(tally_tracker, key=lambda x: x[0]))
