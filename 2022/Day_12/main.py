from enum import Enum
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

class Directions(Enum):
    Up = (-1, 0)
    Down = (1, 0)
    Left = (0, -1)
    Right = (0, 1)

class Point:
    def __init__(self, name, value):
        self.Name = name
        self.Value = value
        self.PossibleSteps: set(Directions) = set()
        self.ShortestPath = -1
        self.Parents: set(Directions) = set()
        self.Dead = False
        pass

    def assignParent(self, parent: Directions):
        self.Parents.add(parent)

    def kill(self):
        self.Dead = True

def printGrid(grid):
    for line in grid:
        for point in line:
            dirs = []
            for d in point.PossibleSteps:
                if d is Directions.Down:
                    dirs.append("D")
                elif d is Directions.Up:
                    dirs.append("U")
                elif d is Directions.Left:
                    dirs.append("L")
                elif d is Directions.Right:
                    dirs.append("R")

            print(f'[{point.Value} : {"/".join(dirs)}]', end=" ")
        
        print()

def printAlphaGrid(grid):
    with open(r"Output.txt", "a") as outFile:
        outFile.write("\n".join(["".join([f'{"#".center(3)}|' if p.Dead else f'{str(p.ShortestPath).rjust(3,"0")}|' if p.ShortestPath > 0 else f'{p.Name.center(3)}|' for p in line]) for line in grid]))
        outFile.write("\n\n")

def getLetterValue(letter: chr) -> int:
    return (ord(letter) - 96) if letter.islower() else 0 if letter == "S" else 27

def getInput(fileName):
    global GRID_HEIGHT
    global GRID_WIDTH
    global PointGrid

    file = open(fileName, 'r')
    
    input = [[Point(c, getLetterValue(c)) for c in l.strip()] for l in file.readlines()]
    GRID_HEIGHT = len(input)
    GRID_WIDTH = len(input[0])

    #Gather All Steps
    for row in range(GRID_HEIGHT):
        for column in range(GRID_WIDTH):
            thisPoint = input[row][column]

            if thisPoint.Value == ENDING_VALUE:
                thisPoint.ShortestPath = 0
                continue
        
            # upward move
            if row > 0: 
                uMove = input[row-1][column]
                if validStep(thisPoint.Value, uMove.Value):
                    thisPoint.PossibleSteps.add(Directions.Up)

            # down move
            if row < GRID_HEIGHT - 1: 
                dMove = input[row+1][column]
                if validStep(thisPoint.Value, dMove.Value):
                    thisPoint.PossibleSteps.add(Directions.Down)

            # left move
            if column > 0: 
                lMove = input[row][column-1]
                if validStep(thisPoint.Value, lMove.Value):
                    thisPoint.PossibleSteps.add(Directions.Left)

            # right move
            if column < GRID_WIDTH - 1: 
                rMove = input[row][column+1]
                if validStep(thisPoint.Value, rMove.Value):
                    thisPoint.PossibleSteps.add(Directions.Right)
    
    #Assign All Parents
    for row in range(GRID_HEIGHT):
        for column in range(GRID_WIDTH):
            thisPoint = input[row][column]
        
            for d in thisPoint.PossibleSteps:
                dr, dc = d.value
                match d:
                    case Directions.Up:
                        input[row+dr][column+dc].assignParent(Directions.Down)
                    case Directions.Down:
                        input[row+dr][column+dc].assignParent(Directions.Up)
                    case Directions.Left:
                        input[row+dr][column+dc].assignParent(Directions.Right)
                    case Directions.Right:
                        input[row+dr][column+dc].assignParent(Directions.Left)

    #if USE_LOGGING: printGrid(input)
    return input

EndPoint = None

def validStep(here, there):
    # If Reverse, allow all steps up but at most one step down
    # If Regular, allow all steps down but at most one step up
    # Changed to not allow reverse direction steps because I can visually see on the map that it's not necessary, lots of traps
    if type(there) is not int: return False

    return (there - here >= -1) if REVERSE_SEARCH else (here - there >= -1)

def findPaths(inputGrid, goalCoords):
    gRow, gCol = goalCoords
    
    passUpdates = 1

    rowRange = range(GRID_HEIGHT)
    colRange = range(GRID_WIDTH)
    
    while passUpdates > 0:
        previousRowUpdates = 0
        passUpdates = 0

        for row in rowRange:
            thisRowUpdates = 1

            while (thisRowUpdates > 0):
                thisRowUpdates = 0

                for col in colRange:
                    p: Point = inputGrid[row][col]

                    #if (True or p.ShortestPath < 0): #only do it if we haven't found a shortest path value, might be a mistake
                    bestStep = None
                    for d in p.PossibleSteps:
                        dr, dc = d.value
                        stepPathValue = inputGrid[row+dr][col+dc].ShortestPath + 1

                        if stepPathValue > 0:
                            if bestStep is None or stepPathValue < bestStep:
                                bestStep = stepPathValue

                    if bestStep is not None and (p.ShortestPath < 0 or bestStep < p.ShortestPath):
                        p.ShortestPath = bestStep
                        thisRowUpdates += 1
                        passUpdates += 1

                #if previousRowUpdates > 0 and thisRowUpdates == 0:
                    #break #want to skip the rest and restart

                #previousRowUpdates = thisRowUpdates

        if USE_LOGGING: 
            print(f'Iteration Updates: {passUpdates}')
            printAlphaGrid(inputGrid)

    killings = 1
    while killings > 0:
        killings = 0

        # check for dead points. Might be problematic since I'm doing incremental updates
        for row in rowRange:
            for col in colRange:
                p: Point = inputGrid[row][col]

                if p.Dead or (row == gRow and col == gCol): continue

                #The point is dead if no points that can step to it are live or none of them have a 1 higher step value
                dead = True
                for pd in p.Parents:
                    pr, pc = pd.value
                    parentPoint = inputGrid[row+pr][col+pc]
                    dead = dead and (parentPoint.Dead or (p.ShortestPath >= 0 and parentPoint.ShortestPath >=0 and parentPoint.ShortestPath != p.ShortestPath+1))

                if dead: 
                    p.kill()
                    killings += 1
                    continue

        if USE_LOGGING: 
            print(f'Deaths: {killings}')
            printAlphaGrid(inputGrid)

        
"""         for d in Directions:
            adjRow, adjCol = d.value
            adjPoint:Point = inputGrid[row + adjRow][col + adjCol]
            oppDirection = None
            stepLength = myPoint.ShortestPath + 1

            match d:
                case Directions.Up:
                    oppDirection = Directions.Down
                case Directions.Down:
                    oppDirection = Directions.Up
                case Directions.Left:
                    oppDirection = Directions.Right
                case Directions.Right:
                    oppDirection = Directions.Left

            if adjPoint.PossibleSteps.__contains__(oppDirection): #if adjacent cell can get to me
                if adjPoint.ShortestPath < 0:
                    adjPoint.ShortestPath = stepLength
                elif adjPoint.ShortestPath > stepLength:
                    adjPoint.PossibleSteps.clear()
                    adjPoint.ShortestPath = stepLength """

def getTargetCoordinates(input):
    global EndPoint

    startingPoint = (-1, -1)
    for i, row in enumerate(input):
        matches = [x for x in range(len(row)) if row[x].Value == STARTING_VALUE]
        if (matches):
            startingPoint = (i, matches[0])
        
        matches = [x for x in range(len(row)) if row[x].Value == ENDING_VALUE]
        if (matches):
            EndPoint = (i, matches[0])

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

    STARTING_VALUE = 27 if REVERSE_SEARCH else 0
    ENDING_VALUE = 0 if REVERSE_SEARCH else 27

    startTime = time.perf_counter()

    file = 'example.txt' if USE_DEMO else 'input1.txt'

    input = getInput(file)
    startIndex = getTargetCoordinates(input)
    findPaths(input, startIndex)
    solution = input[startIndex[0]][startIndex[1]].ShortestPath

    endtime = time.perf_counter()

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])