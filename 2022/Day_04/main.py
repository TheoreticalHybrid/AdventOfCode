import time
import os

useLogging = False

def getRange(input):
    s = input.split('-')
    lowerBound = int(s[0])
    upperBound = int(s[1])
    return list(range(lowerBound, upperBound+1))

def getAssignmentPairs(fileName):
    file = open(fileName, 'r')
    input =  [list(map(lambda section: getRange(section), x.strip().split(','))) for x in file.readlines()]

    if useLogging: print(input)

    return input

def isContained(input, requireSubset):
    input.sort(key=lambda l: len(l))
    return all(section in input[1] for section in input[0]) if requireSubset else any(section in input[1] for section in input[0])

#start of main
useDemo = False
partOne = False
solution = 0

startTime = time.time()

file = 'example.txt' if useDemo else 'input1.txt'
assPairs = getAssignmentPairs(file)

for pair in assPairs:
    solution += 1 if isContained(pair, partOne) else 0

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)