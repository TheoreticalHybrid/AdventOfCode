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
    file = open(fileName, 'r')
    
    input = [[x.strip().split(',') for x in line.strip().split(':')] for line in file.readlines()]

    points = []
    for sb in input:
        s,b = sb[0],sb[1]
        sensorCoords = (int(s[0].strip()[12:]), int(s[1].strip()[2:]))
        beaconCoords = (int(b[0].strip()[23:]), int(b[1].strip()[2:]))
        points.append((sensorCoords, beaconCoords))

    if USE_LOGGING: print(points)

    return points

def getRowData(sensorData, targetRow, excludeSandB, minValue, maxValue):
    rowBlackouts = set()
    sensors = []
    beacons = []
    for d,datum in enumerate(sensorData):
        sY,sX= datum[0]
        bY,bX = datum[1]

        sensors.append((sX,sY))
        beacons.append((bX,bY))

        # determine beacon distance
        distance = abs(sX - bX) + abs(sY - bY)

        # I need sX + or - Dx to equal targetRow
        # Dx is every number in range(distance)
        # So I need to first determine if targetRow-Sx is in range 
        # or if sX-targetRow is in range
        for i in [targetRow-sX, sX-targetRow]:
            if 0 <= i <= distance:
                dY = distance-i
                sortedY = sorted([sY-dY, sY+dY])
                if minValue is not None: sortedY[0] = max(minValue, sortedY[0])
                if maxValue is not None: sortedY[1] = min(maxValue, sortedY[1])
                YRange = list(range(sortedY[0], sortedY[1]+1))
                rowBlackouts.update(YRange)

        # for i in range(distance):
        #     dX,dY = i, distance-i

        #     sortedY = sorted([sY-dY, sY+dY])
        #     YRange = list(range(sortedY[0], sortedY[1]+1))

        #     if sX-dX not in ImpossibleSpots: ImpossibleSpots[sX-dX] = set()
        #     ImpossibleSpots[sX-dX].update(YRange)
        #     if sX+dX not in ImpossibleSpots: ImpossibleSpots[sX+dX] = set()
        #     ImpossibleSpots[sX+dX].update(YRange)

    if excludeSandB:
        for sensor in sensors:
            if sensor[0] == targetRow:
                rowBlackouts.discard(sensor[1])
        for beacon in beacons:
            if beacon[0] == targetRow:
                rowBlackouts.discard(beacon[1])

    return rowBlackouts

def findBeacon(sensorData, maxValue):

    # for row in range(maxValue+1):
    #     if USE_LOGGING: print(f'Checking row {row}')
    #     rowData = getRowData(sensorData, row, False, 0, maxValue)
    #     if len(rowData) < maxValue:
    #         print(f'{row}', end=': ')
    #         print(f'{set(range(maxValue+1)) - rowData}')

    for i in (range(maxValue)):
        if USE_LOGGING: print(f'i: {i}')
        for j in (range(maxValue)):
            if USE_LOGGING: print(f'j: {j}', end='\r')
            beaconFound = True

            for d,datum in enumerate(sensorData):
                sX,sY = datum[0]
                bX,bY = datum[1]

                # determine beacon distance
                beaconDistance = abs(sX - bX) + abs(sY - bY)
                cellDistance = abs(sX - i) + abs(sY - j)
                if cellDistance <= beaconDistance:
                    beaconFound = False
                    break

            if beaconFound: return (i,j)
            

def main(argv):
    global USE_DEMO
    global USE_LOGGING
    global PART_ONE

    global ImpossibleSpots
    
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

    if PART_ONE:
        targetRow = 10 if USE_DEMO else 2000000
        row = getRowData(input, targetRow, True, None, None)
        solution = len(row)
        #if USE_LOGGING: print(sorted(list(ImpossibleSpots[targetRow])))
    else:
        maxV = 20 if USE_DEMO else 4000000
        x = findBeacon(input, maxV)
        solution = x

    endtime = time.perf_counter()

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])