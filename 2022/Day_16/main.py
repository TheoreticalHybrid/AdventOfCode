from enum import Enum
import getopt
from itertools import chain, permutations
import sys
import time
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = True

class Valve:
    def __init__(self, name, rate):
        self.Name = name
        self.FlowRate = rate
        #self.LinkedValves = []

MoveDictionary = {}

def getInput(fileName):
    global MoveDictionary

    file = open(fileName, 'r')
    
    input = [[data.strip() for data in row.split(';')] for row in file.readlines()]

    valves = []
    for row in input:
        valveName = row[0][6:8]
        valveRate = int(row[0][23:])
        valveTunnels = [tunnel.strip() for tunnel in row[1][22:].split(',')]
        v = Valve(valveName, valveRate)
        valves.append(v)
        MoveDictionary[valveName] = valveTunnels

    # for key, value in MoveDictionary.items():
    #     targetValve = list(filter(lambda v: v.Name == key, valves))[0]
    #     for tunnel in value:
    #         tunnelValve = list(filter(lambda v: v.Name == tunnel, valves))[0]
    #         targetValve.LinkedValves.append(tunnelValve)

    if USE_LOGGING:
        for v in valves:
            print(f'{v.Name} ({v.FlowRate})')
            # for t in v.LinkedValves:
            #     print(f'\t{t.Name} ({t.FlowRate})')

    return valves

def getBestPath(currentPathStack, goalNode, currentBestPathLength):
    global MoveDictionary

    currentNode = currentPathStack[-1]
    bestPath = None

    if currentBestPathLength is not None and currentPathStack <= len(currentPathStack): return None

    for possibleStep in MoveDictionary[currentNode]:
        if possibleStep not in currentPathStack:
            testStack = list(currentPathStack)
            testStack.append(possibleStep)
            if possibleStep == goalNode: return testStack
            else:
                trialPath = getBestPath(testStack, goalNode, currentBestPathLength)
                if trialPath is not None and (bestPath is None or len(trialPath) < len(bestPath)):
                    bestPath = trialPath

    return bestPath

BestPathDict = None


def getOptimalPressureRelease(valveSet):
    global BestPathDict
    targetValves = list(filter(lambda v: v.FlowRate > 0, valveSet))
    startingValve = list(filter(lambda v: v.Name == "AA", valveSet))[0]

    #build optimal path dictionary
    BestPathDict = {valve.Name: {usefulValve.Name: None for usefulValve in list(filter(lambda tv: tv.Name != valve.Name, targetValves))} for valve in valveSet}
    for valveName, pathDict in BestPathDict.items():
        for targetValveName in pathDict.keys():
            bestPath = getBestPath([valveName], targetValveName, None)
            pathDict[targetValveName] = len(bestPath)

    bestPressureRelease = 0

    totalTimeAllowed = 30
    currentMinute = 0
    while currentMinute < totalTimeAllowed:
        if not any(targetValves):
            break

        bestMoveValve = None
        bestMoveCost = None
        bestMoveValue = None
        # get most beneficial reamaining target valve
        for valve in targetValves:
            # figure out best path from current valve
            currentCost = BestPathDict[startingValve.Name][valve.Name]
            currentValue = valve.FlowRate * (totalTimeAllowed - (currentCost + currentMinute))

            if bestMoveValue is None or currentValue > bestMoveValue or (currentValue == bestMoveValue and currentCost < bestMoveCost):
                bestMoveValve = valve
                bestMoveCost = currentCost
                bestMoveValue = currentValue

        # accumulate pressure value
        bestPressureRelease += bestMoveValue

        # remove valve from targetValve
        targetValves.remove(bestMoveValve)

        # reassign startingValve to currentValve
        startingValve = bestMoveValve

        # adjust currentMinute accordingly
        currentMinute += bestMoveCost

    return bestPressureRelease


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
    
    USE_DEMO = True
    #USE_LOGGING = True
    #PART_ONE = False

    startTime = time.perf_counter()

    file = 'example.txt' if USE_DEMO else 'input1.txt'

    valves = getInput(file)
    solution = getOptimalPressureRelease(valves)

    endtime = time.perf_counter()

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])