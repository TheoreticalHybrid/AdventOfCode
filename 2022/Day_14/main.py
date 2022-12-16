from enum import Enum
import getopt
from itertools import chain
import sys
import time
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = True

def getInput(fileName):
    global GRID_HEIGHT
    global GRID_WIDTH
    global PointGrid

    file = open(fileName, 'r')
    
    input = [[tuple(int(c) for c in coord.strip('()').split(',')) for coord in rock.strip().split(" -> ")] for rock in file.readlines()]

    if USE_LOGGING: print(input)

    return input

def dropSand(input):
    sandStartingPoint = (500,0)

    #build rockFormations
    takenSpots: dict() = {}
    for rock in input:
        for i in range(len(rock)-1):
            #define line
            point1x, point1y = rock[i]
            point2x, point2y = rock[i+1]

            if (point1x == point2x):
                if point1x not in takenSpots: takenSpots[point1x] = set()
                sortedPoints = sorted([point1y, point2y])
                takenSpots[point1x].update(list(range(sortedPoints[0], sortedPoints[1]+1)))
            elif (point1y == point2y):
                sortedPoints = sorted([point1x, point2x])
                for x in range(sortedPoints[0], sortedPoints[1]+1):
                    if x not in takenSpots: takenSpots[x] = set()
                    takenSpots[x].add(point1y)

    lowestY = max(set(chain(*takenSpots.values())))
    floor = lowestY + 2

    sandCount = 0
    sandStopped = True
    while sandStopped:
        sandStopped = False
        sandX, sandY = sandStartingPoint

        if sandX in takenSpots and sandY in takenSpots[sandX]:
            break

        while sandY <= lowestY if PART_ONE else sandY < floor:

            if PART_ONE or sandY < floor-1:
                if sandX not in takenSpots or sandY+1 not in takenSpots[sandX]:
                    sandY += 1
                    continue
                elif sandX-1 not in takenSpots or sandY+1 not in takenSpots[sandX-1]:
                    sandX -= 1
                    sandY += 1
                    continue
                elif sandX+1 not in takenSpots or sandY+1 not in takenSpots[sandX+1]:
                    sandX += 1
                    sandY += 1
                    continue
            
            if sandX not in takenSpots: takenSpots[sandX] = set()
            takenSpots[sandX].add(sandY)
            sandStopped = True
            sandCount += 1
            break

    return sandCount

def main(argv):
    global USE_DEMO
    global USE_LOGGING
    global PART_ONE
    
    solution = 0

    opts, args = getopt.getopt(argv, "elt")
    for opt, arg in opts:
        match opt:
            case "-e":
                USE_DEMO = True
            case "-l":
                USE_LOGGING = True
            case "-t":
                PART_ONE = False
    
    #USE_DEMO = True
    #USE_LOGGING = True
    #PART_ONE = False

    startTime = time.perf_counter()

    file = 'example.txt' if USE_DEMO else 'input1.txt'

    input = getInput(file)

    solution = dropSand(input)

    endtime = time.perf_counter()

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])