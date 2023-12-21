import time
from copy import deepcopy
import itertools

USE_LOGGING = True
USE_DEMO = True
PART_ONE = False

StartingPoint = None

def getInput(fileName):
    global StartingPoint
    file = open(fileName, 'r')

    input = []
    
    for i, line in enumerate(file.readlines()):
        lineList = [c for c in line.strip()]
        input.append(lineList)
        if 'S' in lineList: StartingPoint = (i, lineList.index('S'))

    return input

Endpoints = []

# Recursive solution, not viable
def getPlotCount_Recursive(grid, steps, path):
    global Endpoints
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    count = 0

    if len(path) == steps + 1: # + 1 because starting point is in the path
        if path[-1] in Endpoints: return 0
        else:
            if USE_LOGGING: print(path)
            Endpoints.append(path[-1])
            return 1

    myY,myX = path[-1]
    for dY, dX in directions:
        stepY, stepX = myY + dY, myX + dX

        if 0 <= stepY < len(grid) and 0 <= stepX < len(grid[0]):# and (stepY, stepX) not in path:
            step = grid[stepY][stepX]
            if step in ('.','S'): # I think I just need to count even/odd steps away depending on steps input
                count += getPlotCount_Recursive(grid, steps, path + [(stepY, stepX)])

    return count

def getShortestPath(grid, steps):
    stepMap = deepcopy(grid)
    coordQueue = [StartingPoint]
    stepMap[StartingPoint[0]][StartingPoint[1]] = 0

    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while coordQueue:
        myY,myX = coordQueue.pop(0)
        myStep = stepMap[myY][myX]
        if myStep < steps:
            nextStep = myStep + 1
            for dY,dX in directions:
                stepY, stepX = myY + dY, myX + dX

                # this is for finding the shortest number of steps for a given index
                if 0 <= stepY < len(stepMap) and 0 <= stepX < len(stepMap[0]):
                    step = stepMap[stepY][stepX]
                    if step == '.' or (isinstance(step, int) and step > nextStep):
                        stepMap[stepY][stepX] = nextStep
                        coordQueue.append((stepY, stepX))

    if USE_LOGGING:
        for r in stepMap:
            print(' '.join([str(c) for c in r]))
    
    return sum([len([c for c in r if c == steps]) for r in stepMap])

def getPlotCount(grid, steps):
    stepMap = [[{} for c in r] for r in grid]

    thisGrid = (0,0)
    coordQueue = [(thisGrid, StartingPoint, 0)]
    stepMap[StartingPoint[0]][StartingPoint[1]][thisGrid] = 0

    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while coordQueue:
        thisGrid,myCoord,stepsTaken = coordQueue.pop(0)
        myY, myX = myCoord
        if stepsTaken < steps:
            nextStep = (stepsTaken + 1)
            for i,d in enumerate(directions):
                dY,dX = d
                stepY, stepX = myY + dY, myX + dX

                if not (PART_ONE or (0 <= stepY < len(stepMap) and 0 <= stepX < len(stepMap[0]))):
                    # update step coords and grid coord
                    match i:
                        case 0: stepX = 0
                        case 1: stepX = len(stepMap[0])
                        case 2: stepY = 0
                        case 3: stepY = len(stepMap)
                    thisGrid = (thisGrid[0] + dY, thisGrid[1] + dX)

                if 0 <= stepY < len(stepMap) and 0 <= stepX < len(stepMap[0]):
                    step = grid[stepY][stepX]
                    if step in ('.', 'S') and (thisGrid not in stepMap[stepY][stepX]):
                        stepMap[stepY][stepX][thisGrid] = nextStep % 2
                        coordQueue.append((thisGrid, (stepY, stepX), nextStep))

    if USE_LOGGING:
        for r in stepMap:
            print(' '.join([str(c) for c in r]))
    
    goal = steps % 2
    return sum([sum([len([v for k,v in col.items() if v == goal]) for col in row]) for row in stepMap])

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

solution = 0

if PART_ONE:
    solution = getPlotCount(input, 6 if USE_DEMO else 64)
    if USE_LOGGING: print(sorted(Endpoints))
else:
    if USE_DEMO:
        for steps,output in [(6,16),(10,50),(50,1594),(100,6536),(500,167004),(1000,668697),(5000,16733044)]:
            subStart = time.time()
            s = getPlotCount(input, steps)
            if s != output: raise ValueError(f'Test failed for input {steps}. Got {s}')
            subEnd = time.time()
            if USE_LOGGING: print(f'Test {steps} finished in {subEnd - subStart}')

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)