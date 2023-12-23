import time
from copy import deepcopy
import itertools

USE_LOGGING = False
USE_DEMO = True
PART_ONE = True

def getInput(fileName):
    file = open(fileName, 'r')

    input = [[c for c in r.strip()] for r in file.readlines()]

    return input

def findLongestPath_Smart(input):
    pathSegments = {}

    startingPoint = input[0].index('.')
    endingPoint = input[-1].index('.')
    pathQueue = [([(0,startingPoint)], None)]

    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    slopes = ['<', '>', '^', 'v']

    while pathQueue:
        pathObj = pathQueue.pop(0)
        myPath = pathObj[0]
        myY,myX = myPath[-1]

        forbiddenPath = pathObj[1]

        if myPath[-1] == (len(input)-1, endingPoint):
            if myPath[0] not in pathSegments: pathSegments[myPath[0]] = {}
            pathSegments[myPath[0]] = (len(myPath), [(myPath[-1])])
        else:
            paths = []
            for i,d in enumerate(directions):
                dY,dX = d
                stepY, stepX = myY + dY, myX + dX

                if (stepY, stepX) not in myPath and (stepY, stepX) != forbiddenPath and 0 <= stepY < len(input) and 0 <= stepX < len(input[0]):
                    step = input[stepY][stepX]
                    if (not PART_ONE or step not in ('#', slopes[i])) and step in ['.'] + slopes:
                        paths.append((stepY,stepX))
                        #pathQueue.append(myPath + [(stepY, stepX)])
            
            if len(paths) == 1:
                pathQueue.append((myPath + paths, None)) # could pass through forbiddenPath here but I don't think it matters
            else:
                if myPath[0] not in pathSegments: pathSegments[myPath[0]] = {}
                pathSegments[myPath[0]] = (len(myPath), paths)

                for p in paths:
                    pathQueue.append(([p], myPath[-1]))

    longestPath = 0
    fullPaths = []
    fpq = [[(0,startingPoint)]]
    while fpq:
        fp = fpq.pop(0)
        segmentKey = fp[-1]
        _, paths = pathSegments[segmentKey]
        for path in paths:
            if path not in fp:
                if path == endingPoint:
                    fpl = sum([pathSegments[k][0] for k in fp])
                    longestPath = max(longestPath, fpl)
                elif path in pathSegments:
                    newPath = fp + [path]
                    fpq.append(newPath)

    return longestPath

# not viable for part 2 real input
def findLongestPath(input):
    # pathLengthMap = deepcopy(input)

    startingPoint = input[0].index('.')
    endingPoint = input[-1].index('.')

    #pathLengthMap[0][startingPoint] = 0
    pathQueue = [[(0,startingPoint)]]

    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    slopes = ['<', '>', '^', 'v']

    fullPaths = []

    while pathQueue:
        myPath = pathQueue.pop(0)
        myY,myX = myPath[-1]
        # myStep = input[myY][myX]
        if (myY,myX) == (len(input)-1, endingPoint): 
            fullPaths.append(myPath)
        else:
            #nextStep = myStep + 1
            for i,d in enumerate(directions):
                dY,dX = d
                stepY, stepX = myY + dY, myX + dX

                # this is for finding the shortest number of steps for a given index
                if (stepY, stepX) not in myPath and 0 <= stepY < len(input) and 0 <= stepX < len(input[0]):
                    step = input[stepY][stepX]
                    if (not PART_ONE or step not in ('#', slopes[i])) and step in ['.'] + slopes:
                        #pathLengthMap[stepY][stepX] = nextStep
                        pathQueue.append(myPath + [(stepY, stepX)])

    longestPath = 0
    for path in fullPaths:
        pathLength = len(path) - 1
        if USE_LOGGING: print(f'Found path of length {pathLength}')
        longestPath = max(longestPath, pathLength)

    return longestPath

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

solution = findLongestPath_Smart(input)

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)