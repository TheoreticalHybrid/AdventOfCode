import time
import os
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

def getInput(fileName):
    file = open(fileName, 'r')
    input = [[int(y) for y in x.strip()] for x in file.readlines()]

    if USE_LOGGING: printGrid(input)

    return input

def printGrid(grid):
    for row in grid:
        print(''.join([str(n) for n in row]))

def getInternalTreeCount(grid):
    count = 0

    #I think I want to create 2 list for each internal character, one for horizontal and one for vertical
    #Then I want to take each of those lists and split at the character index, excluding it in each
    #With those 4 lists, if my character is larger than the largest integer in the list, then it should be included

    #Hell yeah, that approach set me up for part 2

    #build axes swap grid
    tiltGrid = [[grid[x][y] for x in range(len(grid))] for y in range(len(grid[0]))]

    for i in range(1, len(grid[0])-1):
        for j in range(1, len(grid) - 1):
            horizontalList = grid[i]
            verticalList = tiltGrid[j]
            treeSize = horizontalList[j]

            if (treeSize > max(horizontalList[:j])): #view from west
                count += 1
                continue
            elif (treeSize > max(horizontalList[j+1:])): #view from east
                count += 1
                continue
            elif (treeSize > max(verticalList[:i])): #view from north
                count += 1
                continue
            if (treeSize > max(verticalList[i+1:])): #view from south
                count += 1
                continue

    return count

def getTreeView(lineOfSight, myHeight):
    if lineOfSight is None: return 0
    
    view = 0

    for tree in lineOfSight:
        view += 1
        if (tree >= myHeight): break

    return view

def getBestScenicScore(grid):
    score = 0

    #build axes swap grid
    tiltGrid = [[grid[x][y] for x in range(len(grid))] for y in range(len(grid[0]))]

    for i in range(1, len(grid[0]) - 1):
        for j in range(1, len(grid) - 1):
            horizontalList = grid[i]
            verticalList = tiltGrid[j]
            treeSize = horizontalList[j]

            westView = getTreeView(reversed(horizontalList[:j]), treeSize)
            eastView = getTreeView(horizontalList[j+1:], treeSize)
            northView = getTreeView(reversed(verticalList[:i]), treeSize)
            southView = getTreeView(verticalList[i+1:], treeSize)

            treeScore = westView * eastView * northView * southView
            score = max(score, treeScore)

    return score


#start of main
solution = 0

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'

treeGrid = getInput(file)

if (PART_ONE):
    solution = (len(treeGrid) * 2) + (len(treeGrid[0]) * 2) - 4 #2L + 2W - (4 corners getting counted twice)
    solution += getInternalTreeCount(treeGrid)
else:
    solution = getBestScenicScore(treeGrid)

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime)