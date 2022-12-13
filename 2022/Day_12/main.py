import time
import sys
from typing import List

USE_LOGGING = True
USE_DEMO = False
PART_ONE = True

REVERSE_SEARCH = True
STARTING_VALUE = 27 if REVERSE_SEARCH else 0
ENDING_VALUE = 0 if REVERSE_SEARCH else 27

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

def printGrid(grid):
    print()
    for line in grid:
        print("".join(['.' if (type(c) is int and 0 < c < 27) else str(c) for c in line]))

def validStep(here, there):
    # If Reverse, allow all steps up but at most one step down
    # If Regular, allow all steps down but at most one step up
    return type(there) is int and ((there - here >= -1) if REVERSE_SEARCH else (here - there >= -1))

def findPaths(inputGrid, startingPoint, depth):
    global MoveStack
    global MinimumPathLength
    global StepChecks

    if USE_LOGGING and depth % 100 == 0: print(f'Depth: {depth}')
    StepChecks += 1

    #short circuit if I'm already longer than a found path
    if MinimumPathLength > 0 and len(MoveStack) >= MinimumPathLength: 
        if USE_LOGGING: print("BZZT Short Circuit")
        return

    startRow, startCol = startingPoint
    myValue = inputGrid[startRow][startCol]

    #todo: prioritize more likely steps
    
    # upward move
    if startRow > 0: 
        uMove = inputGrid[startRow-1][startCol]

        if validStep(myValue, uMove):
            #push current value onto stack
            MoveStack.append(myValue)
            #update grid with move
            inputGrid[startRow][startCol] = "V" if REVERSE_SEARCH else "^"
            
            #if next step is end then store length of path and return
            if uMove == ENDING_VALUE:
                myPathLength = len(MoveStack)
                if MinimumPathLength < 0 or myPathLength < MinimumPathLength:
                    MinimumPathLength = myPathLength

                if USE_LOGGING:
                    printGrid(input)
                    print(f'Path Length: {myPathLength}')
            else: #recurse
                findPaths(inputGrid, (startRow-1, startCol), depth + 1)

            #reset point and pop value off stack
            inputGrid[startRow][startCol] = MoveStack.pop()

    # down move
    if startRow < GRID_HEIGHT - 1: 
        dMove = inputGrid[startRow+1][startCol]

        if validStep(myValue, dMove):
            #push current value onto stack
            MoveStack.append(myValue)
            #update grid with move
            inputGrid[startRow][startCol] = "^" if REVERSE_SEARCH else "V"

            if dMove == ENDING_VALUE: #if next step is end then store length of path and return
                myPathLength = len(MoveStack)
                if MinimumPathLength < 0 or myPathLength < MinimumPathLength:
                    MinimumPathLength = myPathLength

                if USE_LOGGING:
                    printGrid(input)
                    print(f'Path Length: {myPathLength}')
            else: #recurse
                findPaths(inputGrid, (startRow+1, startCol), depth + 1)

            #reset point and pop value off stack
            inputGrid[startRow][startCol] = MoveStack.pop()

    # left move
    if startCol > 0: 
        lMove = inputGrid[startRow][startCol-1]

        if validStep(myValue, lMove):
            #push current value onto stack
            MoveStack.append(myValue)
            #update grid with move
            inputGrid[startRow][startCol] = ">" if REVERSE_SEARCH else "<"
           
            if lMove == ENDING_VALUE: #if next step is end then store length of path and return
                myPathLength = len(MoveStack)
                if MinimumPathLength < 0 or myPathLength < MinimumPathLength:
                    MinimumPathLength = myPathLength

                if USE_LOGGING:
                    printGrid(input)
                    print(f'Path Length: {myPathLength}')
            else: #recurse
                findPaths(inputGrid, (startRow, startCol-1), depth + 1)

            #reset point and pop value off stack
            inputGrid[startRow][startCol] = MoveStack.pop()

    # right move
    if startCol < GRID_WIDTH - 1: 
        rMove = inputGrid[startRow][startCol+1]

        if validStep(myValue, rMove):
            #push current value onto stack
            MoveStack.append(myValue)
            #update grid with move
            inputGrid[startRow][startCol] = "<" if REVERSE_SEARCH else ">"

            if rMove == ENDING_VALUE: #if next step is end then store length of path and return
                myPathLength = len(MoveStack)
                if MinimumPathLength < 0 or myPathLength < MinimumPathLength:
                    MinimumPathLength = myPathLength

                if USE_LOGGING:
                    printGrid(input)
                    print(f'Path Length: {myPathLength}')
            else: #recurse
                findPaths(inputGrid, (startRow, startCol+1), depth + 1)
            
            
            #reset point and pop value off stack
            inputGrid[startRow][startCol] = MoveStack.pop()

    return

def getStartingCoordinates(input):
    for i, row in enumerate(input):
        try:
            startIndex = row.index(STARTING_VALUE)
            if (startIndex > -1):
                return (i, startIndex)
        except ValueError:
            pass

#start of main
solution = 0

startTime = time.perf_counter()

file = 'example.txt' if USE_DEMO else 'input1.txt'

input = getInput(file)
startIndex = getStartingCoordinates(input)
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