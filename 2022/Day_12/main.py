from enum import Enum
import getopt
import sys
import time
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

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

    def reset(self):
        self.Dead = False
        self.ShortestPath = -1

def printAlphaGrid(grid):
    with open(r"Output.txt", "a") as outFile:
        outFile.write("\n".join(["".join([f'{"#".center(3)}|' if p.Dead else f'{str(p.ShortestPath).rjust(3,"0")}|' if p.ShortestPath > 0 else f'{p.Name.center(3)}|' for p in line]) for line in grid]))
        outFile.write("\n\n")

def getLetterValue(letter: chr) -> int:
    return (ord(letter) - 96) if letter.islower() else 1 if letter == "S" else 26

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
    return (here - there >= -1)

def findPathsPart1(inputGrid, goalCoords):
    gRow, gCol = goalCoords
    
    passUpdates = 1

    rowRange = range(GRID_HEIGHT)
    colRange = range(GRID_WIDTH)
    
    while passUpdates > 0:
        passUpdates = 0

        for row in rowRange:
            thisRowUpdates = 1

            while (thisRowUpdates > 0):
                thisRowUpdates = 0

                for col in colRange:
                    p: Point = inputGrid[row][col]

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

    """ killings = 1
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
                    continue """

    if USE_LOGGING: 
        printAlphaGrid(inputGrid)

def getTargetCoordinates(input):
    global EndPoint

    startingPoint = [(i,j) for i in range(GRID_HEIGHT) for j in range(GRID_WIDTH) if input[i][j].Name == "S"][0]
    EndPoint = [(i,j) for i in range(GRID_HEIGHT) for j in range(GRID_WIDTH) if input[i][j].Name == "E"][0]

    return startingPoint

def main(argv):
    global USE_DEMO
    global USE_LOGGING
    
    solution = 0

    opts, args = getopt.getopt(argv, "elro")
    for opt, arg in opts:
        match opt:
            case "-e":
                USE_DEMO = True
            case "-l":
                USE_LOGGING = True
    
    #USE_DEMO = True
    #USE_LOGGING = True

    startTime = time.perf_counter()

    file = 'example.txt' if USE_DEMO else 'input1.txt'

    input = getInput(file)
    startIndex = getTargetCoordinates(input)
    input[EndPoint[0]][EndPoint[1]].ShortestPath = 0
    findPathsPart1(input, startIndex)

    if PART_ONE:
        solution = input[startIndex[0]][startIndex[1]].ShortestPath
    else:
        minPath = 5000
        for startingPoint in [(i,j) for i in range(GRID_HEIGHT) for j in range(GRID_WIDTH) if input[i][j].Value == 1]:
            shortPath = input[startingPoint[0]][startingPoint[1]].ShortestPath
            if shortPath > 0: minPath = min(minPath, shortPath)

        solution = minPath

    endtime = time.perf_counter()

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])