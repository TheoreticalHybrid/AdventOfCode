import time
import os
import re
from itertools import product
import copy

USE_LOGGING = False
USE_DEMO = False

Map = []
BaseMap = []

def getInput(fileName):
    global Map
    global BaseMap
    file = open(fileName, 'r')
    Map = [[c for c in line.strip()] for line in file.readlines()]
    BaseMap = copy.deepcopy(Map)

    guardStartingIndex = (0,0)
    guardStartingDirection = (0,0) #going to use coordinate directions like (-1,0) for up

    for i, line in enumerate(Map):
        if '>' in line:
            guardStartingDirection = (0,1)
            guardStartingIndex = (i,line.index('>'))
            break
        elif '<' in line:
            guardStartingDirection = (0,-1)
            guardStartingIndex = (i,line.index('<'))
            break
        elif '^' in line:
            guardStartingDirection = (-1,0)
            guardStartingIndex = (i,line.index('^'))
            break
        elif 'v' in line:
            guardStartingDirection = (1,0)
            guardStartingIndex = (i,line.index('v'))
            break

    input = (guardStartingIndex, guardStartingDirection)
    if USE_LOGGING:
        for line in Map: print(line)
        print('\n')
        print(f'Guard Starting Index: {guardStartingIndex}')
        print(f'Guard Starting Direction: {guardStartingDirection}')

    return input

def findDistinctPositionsCount(input):
    directions = [(-1,0), (0,1), (1,0), (0,-1)]
    visitedSpaces = set()
    guardPosition = input[0]
    guardDirectionIndex = directions.index(input[1])
    lowerEdge, rightEdge = len(Map), len(Map[0])

    nextSpace = tuple(map(lambda i, j: i + j, guardPosition, directions[guardDirectionIndex]))
    while 0 <= nextSpace[0] < lowerEdge and 0 <= nextSpace[1] < rightEdge:
        visitedSpaces.add(guardPosition)
        thisMapChar = Map[guardPosition[0]][guardPosition[1]]
        
        if Map[nextSpace[0]][nextSpace[1]] == '#':
            guardDirectionIndex = (guardDirectionIndex + 1) % 4
        else:
            Map[guardPosition[0]][guardPosition[1]] = ('' if thisMapChar in ['.','<','>','^','v' ] else thisMapChar) + f'{guardDirectionIndex}'
            guardPosition = nextSpace

        nextSpace = tuple(map(lambda i, j: i + j, guardPosition, directions[guardDirectionIndex]))

    visitedSpaces.add(guardPosition) #add the final space before exiting the map
    thisMapChar = Map[guardPosition[0]][guardPosition[1]]
    Map[guardPosition[0]][guardPosition[1]] = ('' if thisMapChar in ['.','<','>','^','v' ] else thisMapChar) + f'{guardDirectionIndex}'

    if USE_LOGGING:
        for line in Map: print(''.join([c if c in ['.','#'] else 'X' for c in line]))
        print()
        for line in Map: print(line)

    return len(visitedSpaces)

def findNumberOfObstructionPositions(input):
    count = 0
    directions = [(-1,0), (0,1), (1,0), (0,-1)]
    lowerEdge, rightEdge = len(Map), len(Map[0])

    guardPosition = input[0]

    #build dictionary of existing obstructions
    obs = dict()
    for i, row in enumerate(Map):
        obs[i] = [j for j,x in enumerate(row) if x == '#']

    mapChar = Map[guardPosition[0]][guardPosition[1]]
    gd = int(mapChar[0])
    step = tuple(map(lambda x, y: x + y, guardPosition, directions[gd]))

    goodOnes = dict()
    checkedPositions = set()

    while 0 <= step[0] < lowerEdge and 0 <= step[1] < rightEdge:
        #only run simulations if the step isn't the starting point and hasn't already been checked
        if step != input[0] and step not in checkedPositions:
            #check if a blocker in that spot would cause an unobstructed turn
            checkedPositions.add(step)
            rightTurnDI = (gd + 1) % 4

            obs[step[0]].append(step[1]) #temporarily add
            mockPosition = tuple(guardPosition)
            turningPoints = set()
            while True:
                tp = (mockPosition, rightTurnDI)
                if tp in turningPoints:
                    #found loop
                    if USE_LOGGING: print(f'Found Valid Blocker at {step}')
                    #count += 1
                    if step[0] not in goodOnes: goodOnes[step[0]] = set()
                    if step[1] not in goodOnes[step[0]]:
                        goodOnes[step[0]].add(step[1])
                        count += 1
                    break

                turningPoints.add(tp)
                rtd = directions[rightTurnDI]
                if rtd[0] == 0:
                    #L/R movement
                    if rtd[1] == 1:
                        closest = min((x for x in obs[mockPosition[0]] if x > mockPosition[1]), default=-1)
                        if closest >= 0:
                            mockPosition = (mockPosition[0], closest-1)
                            rightTurnDI = (rightTurnDI + 1) % 4
                        else:
                            #no obstruction found, therefore no loop
                            break
                    else:
                        closest = max((x for x in obs[mockPosition[0]] if x < mockPosition[1]), default=-1)
                        if closest >= 0:
                            mockPosition = (mockPosition[0], closest+1)
                            rightTurnDI = (rightTurnDI + 1) % 4
                        else:
                            break
                else:
                    #U/D Movement
                    if rtd[0] == 1:
                        closest = min((k for k in obs if k > mockPosition[0] and mockPosition[1] in obs[k]), default=-1)
                        if closest >= 0:
                            mockPosition = (closest-1, mockPosition[1])
                            rightTurnDI = (rightTurnDI + 1) % 4
                        else:
                            break
                    else:
                        closest = max((k for k in obs if k < mockPosition[0] and mockPosition[1] in obs[k]), default=-1)
                        if closest >= 0:
                            mockPosition = (closest+1, mockPosition[1])
                            rightTurnDI = (rightTurnDI + 1) % 4
                        else:
                            break
                        
            obs[step[0]].remove(step[1]) #remove temporary obstruction
        
        Map[guardPosition[0]][guardPosition[1]] = mapChar[1:] if len(mapChar) > 1 else '.'
        guardPosition = step
        mapChar = Map[guardPosition[0]][guardPosition[1]]
        gd = int(mapChar[0])
        step = tuple(map(lambda x, y: x + y, guardPosition, directions[gd]))

        if USE_LOGGING and USE_DEMO:
            for line in Map:
                print(line)
            print()

    if USE_LOGGING:
        total = 0
        for k in sorted(list(goodOnes.keys())):
            print(f'{k} - ({len(goodOnes[k])}) - {sorted(list(goodOnes[k]))}')
            total += len(goodOnes[k])
        print(f'Total: {total}')

    return count

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = findDistinctPositionsCount(input)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()
if USE_LOGGING: print('---------PART TWO---------')
startTime = time.time()

solution = findNumberOfObstructionPositions(input)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)