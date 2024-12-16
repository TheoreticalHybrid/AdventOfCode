import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

Map = []
Movements = {'<': (0,-1), '^': (-1,0), '>': (0,1), 'v': (1,0)}

def printMap():
    for line in Map:
        print(''.join(line))
    print()

def getInput(fileName, partTwo):
    global Map
    Map = []
    input = []

    with open(fileName, 'r') as file:
        charTranslations = {'#': ['#','#'], 'O': ['[',']'], '.': ['.','.'], '@': ['@','.']}
        for line in file.readlines():
            if line[0] == '#': 
                newLine = []
                if partTwo:
                    for c in line.strip(): newLine.extend(charTranslations[c])
                else:
                    newLine = [c for c in line.strip()]
                Map.append(newLine)
            elif line[0] in Movements: input.append([c for c in line.strip()])

    if USE_LOGGING:
        printMap()
        for instructionSet in input:
            print(''.join(instructionSet))

    return input

def performMovePt1(robotLocation, move):
    # iterate over each cell in given move direction, keep track of every coordinate until we hit a '.' or a '#'
    # if hitting a '#', do nothing. Else, update first value to '@', and remaining values to 'O'. Then update robotLocation to '.' and return first location
    cellUpdates = []
    i,j = robotLocation
    moveI, moveJ = move
    nextI, nextJ = i + moveI, j + moveJ
    while Map[nextI][nextJ] == 'O':
        cellUpdates.append((nextI, nextJ))
        nextI += moveI
        nextJ += moveJ

    if Map[nextI][nextJ] == '.':
        cellUpdates.append((nextI, nextJ))
        newRobotLocation = None
        for cell in cellUpdates:
            cx, cy = cell
            if newRobotLocation is None:
                newRobotLocation = cell
                Map[cx][cy] = '@'
            else: Map[cx][cy] = 'O'
        Map[i][j] = '.'
        return newRobotLocation
                
    else: return robotLocation

def performMovePt2(robotLocation, move):
    pass

def executeInstructionSet(instructions, partTwo):
    robotLocation = None
    robotChar = '@'
    for i,l in enumerate(Map):
        if robotChar in l:
            robotLocation = (i, l.index(robotChar))
            break

    verboseLogging = False

    lastMove = None
    lastMoveSucceeded = True
    for line in instructions:
        while any(line):
            move = line.pop(0)
            if USE_LOGGING and verboseLogging: print(f'Move {move}:')
            
            if lastMoveSucceeded or move != lastMove:
                nextRobotLocation = performMovePt2 if partTwo else performMovePt1(robotLocation, Movements[move])
                lastMoveSucceeded = robotLocation != nextRobotLocation
                robotLocation = nextRobotLocation
            
            lastMove = move
            if USE_LOGGING and verboseLogging: printMap()

    if USE_LOGGING: printMap()

def getBoxCoordinateScore():
    sum = 0
    for i,l in enumerate(Map):
        for j,c in enumerate(l):
            if c in {'O', '['}:
                sum += (100 * i) + j

    return sum

exampleFile = 'example2.txt'
file = exampleFile if USE_DEMO else 'input1.txt'
problemInput = getInput(file)
#exit()

startTime = time.time()

executeInstructionSet(problemInput)
solution = getBoxCoordinateScore()

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
print('---------PART TWO---------')
problemInput = getInput(file)


startTime = time.time()

solution = fuckItIGuessIWillSaveEachOneAndLookManually(size, problemInput)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)