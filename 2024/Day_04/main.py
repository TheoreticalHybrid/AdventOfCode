import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

def getInput(fileName):
    file = open(fileName, 'r')
    input =  [[c for c in line.strip()] for line in file.readlines()]

    if USE_LOGGING: print(input)

    return input

def wordConfirm(input, i, j, iDiff, jDiff):
    myI, myJ = i, j
    maxI, maxJ = len(input) - 1, len(input[0]) - 1

    target = ['X','M','A','S']
    for c in target:
        if myI < 0 or myI > maxI or myJ < 0 or myJ > maxJ or input[myI][myJ] != c: return False
        myI += iDiff
        myJ += jDiff

    return True

def confirmXMAS(input, i, j):
    if input[i][j] != 'A': return False # thorough check

    maxI, maxJ = len(input) - 1, len(input[0]) - 1
    #top left index check and bottom right index check
    if 0 <= i-1 <= maxI and 0 <= j-1 <= maxJ and 0 <= i+1 <= maxI and 0 <= j+1 <= maxJ:
        ends = input[i-1][j-1] + input[i+1][j+1]
        if ends != "MS" and ends != "SM": return False
    else: return False

    #top right index check and bottom left index check
    if 0 <= i-1 <= maxI and 0 <= j+1 <= maxJ and 0 <= i+1 <= maxI and 0 <= j-1 <= maxJ:
        ends = input[i-1][j+1] + input[i+1][j-1]
        return ends == "MS" or ends == "SM"
    else: return False

def findXMAS(input, partTwo):
    count = 0

    for i, row in enumerate(input):
        if partTwo and (i == 0 or i == len(input)): continue #skip the edges
        for j, character in enumerate(row):
            if partTwo:
                if j == 0 or j == len(row): continue #skip the edges
                if character == 'A' and confirmXMAS(input, i, j): count += 1
                    
            elif character == 'X':
                #check reverse
                if wordConfirm(input, i, j, 0, -1): count += 1

                #check forward
                if wordConfirm(input, i, j, 0, 1): count += 1

                #check up
                if wordConfirm(input, i, j, -1, 0): count += 1

                #check down
                if wordConfirm(input, i, j, 1, 0): count += 1

                #check top left
                if wordConfirm(input, i, j, -1, -1): count += 1

                #check top right
                if wordConfirm(input, i, j, -1, 1): count += 1

                #check bottom left
                if wordConfirm(input, i, j, 1, -1): count += 1

                #check bottom right
                if wordConfirm(input, i, j, 1, 1): count += 1

    return count

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = findXMAS(input, False)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()

startTime = time.time()

solution = findXMAS(input, True)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)