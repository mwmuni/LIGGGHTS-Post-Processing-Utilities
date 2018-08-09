import os
import shutil
file_list = []
startswith = {'1_', '2_', '3_'}
endswith = '.liggghts'
for filename in os.listdir('.'):
    if filename.startswith(startswith) and filename.endswith(endswith) and not filename.endswith("boundingBox.vtk"):
        file_list.append([filename, int(filename[len(startswith):-len(endswith)])])
file_list = sorted(file_list, key=lambda file: file[1])
count = 0
for e in file_list:
    e[1] = count
    count += 1
for e in file_list:
    shutil.copy(e[0], 'dump_test/' + startswith + str(e[1]).zfill(4) + endswith)