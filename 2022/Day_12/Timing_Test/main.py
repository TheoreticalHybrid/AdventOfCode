import getopt
import sys
import time
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = True

REACH_OVERRIDE = False
REVERSE_SEARCH = False
STARTING_VALUE = 0
ENDING_VALUE = 0

GRID_HEIGHT = 0
GRID_WIDTH = 0

def getLetterValue(letter: chr) -> int:
    return (ord(letter) - 96) if letter.islower() else 0 if letter == "S" else 27

def getInput(fileName):
    global GRID_HEIGHT
    global GRID_WIDTH
    file = open(fileName, 'r')
    
    input = [[getLetterValue(c) for c in l.strip()] for l in file.readlines()]
    GRID_HEIGHT = len(input)
    GRID_WIDTH = len(input[0])

    return input

MinimumPathLength = -1
MoveStack = []
StepChecks = 0
EndPoint = None

def printGrid(grid):
    print()
    for line in grid:
        print("".join(['.' if (type(c) is int and 0 < c < 27) else str(c) for c in line]))

def validStep(here, there):
    # If Reverse, allow all steps up but at most one step down
    # If Regular, allow all steps down but at most one step up
    # Changed to not allow reverse direction steps because I can visually see on the map that it's not necessary, lots of traps
    if type(there) is not int: return False

    return (there - here >= -1) if REVERSE_SEARCH else (here - there >= -1)

def findPaths(inputGrid, startingPoint, depth):
    global MoveStack
    global MinimumPathLength
    global StepChecks
    global EndPoint

    StepChecks += 1
    if USE_LOGGING and StepChecks % 100000 == 0: print(f'Check #: {StepChecks//1000000}m', end= '\r')

    startRow, startCol = startingPoint
    rowDiff = startRow - EndPoint[0]
    colDiff = startCol - EndPoint[1]

    if MinimumPathLength > 0:        
        minNumMoves = abs(rowDiff) + abs(colDiff)
        if minNumMoves + len(MoveStack) >= MinimumPathLength: #short circuit if the shortest path to the end is going to be longer than the path already found
            return
        
        if len(MoveStack) >= MinimumPathLength: #short circuit if I'm already longer than a found path (probably redundant with above check)
            #if USE_LOGGING: print("BZZT Short Circuit")
            return

    myValue = inputGrid[startRow][startCol]

    #todo: prioritize more likely steps
    prioritizedMoves = []
    otherMoves = []

    startReaching = REACH_OVERRIDE or MinimumPathLength > 0
    
    # upward move
    if startRow > 0: 
        uMove = inputGrid[startRow-1][startCol]
        if validStep(myValue, uMove):
            move = (uMove, "up")
            if startReaching and rowDiff < 0:
                prioritizedMoves.append(move)
            else:
                otherMoves.append(move)

    # down move
    if startRow < GRID_HEIGHT - 1: 
        dMove = inputGrid[startRow+1][startCol]
        if validStep(myValue, dMove):
            move = (dMove, "down")
            if startReaching and rowDiff > 0:
                prioritizedMoves.append(move)
            else:
                otherMoves.append(move)

    # left move
    if startCol > 0: 
        lMove = inputGrid[startRow][startCol-1]
        if validStep(myValue, lMove):
            move = (lMove, "left")
            if startReaching and colDiff < 0:
                prioritizedMoves.append(move)
            else:
                otherMoves.append(move)

    # right move
    if startCol < GRID_WIDTH - 1: 
        rMove = inputGrid[startRow][startCol+1]
        if validStep(myValue, rMove):
            move = (rMove, "right")
            if startReaching and colDiff > 0:
                prioritizedMoves.append(move)
            else:
                otherMoves.append(move)

    prioritizedMoves = sorted(prioritizedMoves, reverse= not REVERSE_SEARCH)
    otherMoves = sorted(otherMoves, reverse= not REVERSE_SEARCH)
    prioritizedMoves.extend(otherMoves)

    for val, direction in prioritizedMoves:
        moveChar = None
        moveRow, moveCol = startRow, startCol

        match direction:
            case "up":
                moveChar = "V" if REVERSE_SEARCH else "^"
                moveRow -= 1
            case "down":
                moveChar = "^" if REVERSE_SEARCH else "V"
                moveRow += 1
            case "left":
                moveChar = ">" if REVERSE_SEARCH else "<"
                moveCol -= 1
            case "right":
                moveChar = "<" if REVERSE_SEARCH else ">"
                moveCol += 1

        
        #push current value onto stack
        MoveStack.append(myValue)
        #update grid with move
        inputGrid[startRow][startCol] = moveChar

        if val == ENDING_VALUE: #if next step is end then store length of path and return
            if EndPoint is None: EndPoint = (moveRow, moveCol)
            myPathLength = len(MoveStack)
            if MinimumPathLength < 0 or myPathLength < MinimumPathLength:
                MinimumPathLength = myPathLength

                if USE_LOGGING:
                    printGrid(inputGrid)
                    print(f'Path Length: {myPathLength}')
        else: #recurse
            findPaths(inputGrid, (moveRow, moveCol), depth + 1)
        
        
        #reset point and pop value off stack
        inputGrid[startRow][startCol] = MoveStack.pop()

    return

def getTargetCoordinates(input):
    global EndPoint

    startingPoint = (-1, -1)
    for i, row in enumerate(input):
        try:
            startIndex = row.index(STARTING_VALUE)
            if (startIndex > -1):
                startingPoint = (i, startIndex)
        except ValueError:
            pass
        
        try:
            endIndex = row.index(ENDING_VALUE)
            if (endIndex > -1):
                EndPoint = (i, endIndex)
        except ValueError:
            pass

    return startingPoint

def main(argv):
    global USE_DEMO
    global USE_LOGGING
    global REVERSE_SEARCH
    global REACH_OVERRIDE
    global STARTING_VALUE
    global ENDING_VALUE
    
    solution = 0

    opts, args = getopt.getopt(argv, "elro")
    for opt, arg in opts:
        match opt:
            case "-e":
                USE_DEMO = True
            case "-l":
                USE_LOGGING = True
            case "-r":
                REVERSE_SEARCH = True
            case "-o":
                REACH_OVERRIDE = True

    
    #USE_DEMO = True
    #USE_LOGGING = True
    #REVERSE_SEARCH = True
    #REACH_OVERRIDE = True
    
    STARTING_VALUE = 27 if REVERSE_SEARCH else 0
    ENDING_VALUE = 0 if REVERSE_SEARCH else 27

    startTime = time.perf_counter()

    file = 'example.txt' if USE_DEMO else 'input1.txt'

    input = getInput(file)
    startIndex = getTargetCoordinates(input)
    sys.setrecursionlimit(GRID_HEIGHT * GRID_WIDTH + 50)

    try:
        findPaths(input, startIndex, 0)
    except RecursionError as re:
        print(f'Recursion error')

    solution = MinimumPathLength

    endtime = time.perf_counter()

    if USE_LOGGING: print(f'Checks: {StepChecks}')

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])