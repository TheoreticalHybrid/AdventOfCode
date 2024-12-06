import time
import os
import re
from itertools import product

USE_LOGGING = False
USE_DEMO = False

Map = []

def getInput(fileName):
    global Map
    file = open(fileName, 'r')
    Map = [[c for c in line.strip()] for line in file.readlines()]

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
        Map[guardPosition[0]][guardPosition[1]] = ('' if thisMapChar in ['.','<','>','^','v' ] else thisMapChar) + f'{guardDirectionIndex}'
        
        if Map[nextSpace[0]][nextSpace[1]] == '#':
            guardDirectionIndex = (guardDirectionIndex + 1) % 4
        else:
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

def createsLoop(startingInfo, testingMap):
    directions = [(-1,0), (0,1), (1,0), (0,-1)]
    guardPosition = startingInfo[0]
    guardDirectionIndex = directions.index(startingInfo[1])
    lowerEdge, rightEdge = len(testingMap), len(testingMap[0])
    
    loopCreated = False
    
    nextSpace = tuple(map(lambda i, j: i + j, guardPosition, directions[guardDirectionIndex]))
    while 0 <= nextSpace[0] < lowerEdge and 0 <= nextSpace[1] < rightEdge:
        thisMapChar = testingMap[guardPosition[0]][guardPosition[1]]
        
        if str(guardDirectionIndex) in thisMapChar:
            loopCreated = True
            break

        testingMap[guardPosition[0]][guardPosition[1]] = ('' if thisMapChar in ['.','<','>','^','v' ] else thisMapChar) + f'{guardDirectionIndex}'
        
        if testingMap[nextSpace[0]][nextSpace[1]] == '#':
            guardDirectionIndex = (guardDirectionIndex + 1) % 4
        else:
            guardPosition = nextSpace

        nextSpace = tuple(map(lambda i, j: i + j, guardPosition, directions[guardDirectionIndex]))

    return loopCreated    

def findNumberOfObstructionPositions(input):
    count = 0
    directions = [(-1,0), (0,1), (1,0), (0,-1)]
    lowerEdge, rightEdge = len(Map), len(Map[0])

    #build dictionary of existing obstructions
    obs = dict()
    for i, row in enumerate(Map):
        obs[i] = [j for j,x in enumerate(row) if x == '#']

    #get potential blocker spots
    blockers = set()
    for i,j in product(range(lowerEdge),range(rightEdge)):
        mapChar = Map[i][j]
        if mapChar not in ['.','#']:
            #split on traveling directions
            for di in [int(c) for c in mapChar]:
                step = tuple(map(lambda x, y: x + y, (i,j), directions[di]))
                # if step in that direction is valid
                if 0 <= step[0] < lowerEdge and 0 <= step[1] < rightEdge and Map[step[0]][step[1]] != '#':
                    #check if a blocker in that spot would cause an unobstructed turn
                    rightTurnDI = (di + 1) % 4
                    rtd = directions[rightTurnDI]

                    obstructed = False
                    if rtd[0] == 0:
                        #L/R movement
                        obstructed = any((x > j if rtd[1] > 0 else x < j) for x in obs[i])
                    else:
                        #U/D movement
                        obstructed = any((k > i if rtd[0] > 0 else k < i) and j in obs[k] for k in obs)

                    if obstructed:
                        blockers.add(step)

    if USE_LOGGING:
        for i in range(len(Map)):
            l = ''
            for j in range(len(Map[0])):
                if (i,j) in blockers:
                    l += '?' # this represents the location of possible blockers
                elif Map[i][j] == '#':
                    l += '#'
                else: l += '.'
            print(l)

    #test each blocker spot
    
    for testBlocker in blockers:
        starterMap = [[c if c == '#' else '.' for c in row] for row in Map]
        starterMap[testBlocker[0]][testBlocker[1]] = '#'
        
        if USE_LOGGING:
            print(f'TESTING BLOCKER: {testBlocker}')
            for line in starterMap: print(''.join(line))

        if createsLoop(input, starterMap):
            if USE_LOGGING: print(f'LOOP DETECTED FOR {testBlocker}')
            count += 1

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