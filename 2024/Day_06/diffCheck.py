import time
import os
import re

file1, file2 = 'Day6-Old.txt', 'Day6-New.txt'
f1Dict, f2Dict = dict(), dict()

file = open(file1, 'r')
for line in file.readlines():
    k, _, v = line.split(' - ')
    f1Dict[int(k)] = set(int(x.strip()) for x in v.strip()[1:-1].split(','))

file = open(file2, 'r')
for line in file.readlines():
    k, _, v = line.split(' - ')
    f2Dict[int(k)] = set(int(x.strip()) for x in v.strip()[1:-1].split(','))

totalDiff = 0
for i in range(len(f1Dict)):
    if i not in f2Dict: f2Dict[i] = set()
    onlyInB = f2Dict[i] - f1Dict[i]
    onlyInA = f1Dict[i] - f2Dict[i]
    if any(onlyInA) or any(onlyInB):
        print(f'{i} - {onlyInA} : {onlyInB}')
        totalDiff = totalDiff - len(onlyInA)
        totalDiff += len(onlyInB)
print(f'Total Difference: {totalDiff}')

exit()

startTime = time.time()

solution = findValidMidSum(input, False)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()
if USE_LOGGING: print('---------PART TWO---------')
startTime = time.time()

solution = findValidMidSum(input, True)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)