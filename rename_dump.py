import os
import shutil
startswithtuple = ('1_', '2_', '3_')
endswith = '.liggghts'
for startswith in startswithtuple:
    file_list = []
    for filename in os.listdir('.'):
        if filename.startswith(startswith) and filename.endswith(endswith) and not filename.endswith("boundingBox.vtk"):
            file_list.append([filename, int(filename[2:-len(endswith)])])
    file_list = sorted(file_list, key=lambda file: file[1])
    count = 0
    for e in file_list:
        e[1] = count
        count += 1
    if not os.path.exists('dump_test/'):
        os.makedirs('dump_test/')
    for e in file_list:
        shutil.copy(e[0], 'dump_test/' + startswith + str(e[1]).zfill(4) + endswith)