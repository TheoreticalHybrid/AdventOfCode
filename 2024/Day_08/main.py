import time
import os
import re
from math import gcd

USE_LOGGING = False
USE_DEMO = False

Map = []

def getInput(fileName):
    global Map
    file = open(fileName, 'r')
    antennas = dict()

    for i, line in enumerate(file.readlines()):
        line = line.strip()
        Map.append([x for x in line])
        for j,c in enumerate(line):
            if c != '.':
                if c not in antennas: antennas[c] = []
                antennas[c].append((i,j))

    if USE_LOGGING:
        print(antennas)

    return antennas

def tupleSubtraction(t1, t2):
    return tuple(map(lambda x, y: x - y, t2, t1))

def tupleAddition(t1, t2):
    return tuple(map(lambda x, y: x + y, t1, t2))

def printMap(antiNodes):
    print()
    for i,line in enumerate(Map):
        printstring = ''
        for j,c in enumerate(line):
            printstring += c if c != '.' or (i,j) not in antiNodes else '#'
        print(printstring)    

def getUniqueAntinodes(input, partTwo):
    bottomRow, rightCol = len(Map), len(Map[0])
    antinodePositions = set()

    for k,v in input.items():
        for i, node in enumerate(v[:-1]):
            for node2 in v[i+1:]:                
                if partTwo:
                    diff = tupleSubtraction(node, node2)
                    divisor = gcd(abs(diff[0]), abs(diff[1]))
                    if divisor > 0: diff = (int(diff[0] / divisor), int(diff[1] / divisor))
                    
                    antinodePositions.add(node) # add current node
                    
                    #add all positions in direction away from node2
                    nextAN = tupleSubtraction(diff, node)
                    while 0 <= nextAN[0] < bottomRow and 0 <= nextAN[1] < rightCol:
                        antinodePositions.add(nextAN)
                        nextAN = tupleSubtraction(diff, nextAN)

                    #add all positions in direction toward node2 (including node2)
                    nextAN = tupleAddition(diff, node)
                    while 0 <= nextAN[0] < bottomRow and 0 <= nextAN[1] < rightCol:
                        antinodePositions.add(nextAN)
                        nextAN = tupleAddition(diff, nextAN)
                    
                else:
                    #outside antinodes
                    diff = tupleSubtraction(node, node2)
                    antiNode = tupleSubtraction(diff, node)
                    if 0 <= antiNode[0] < bottomRow and 0 <= antiNode[1] < rightCol: antinodePositions.add(antiNode)
                    antiNode = tupleAddition(diff, node2)
                    if 0 <= antiNode[0] < bottomRow and 0 <= antiNode[1] < rightCol: antinodePositions.add(antiNode)
                    
                    #inside positions
                    if diff[0] % 3 == 0 and diff[1] % 3 == 0:
                        insideDiff = (int(diff[0] / 3), int(diff[1] / 3))
                        antiNode = tupleAddition(node, insideDiff)
                        if 0 <= antiNode[0] < bottomRow and 0 <= antiNode[1] < rightCol: antinodePositions.add(antiNode)
                        insideDiff = (diff[0] * -1, diff[1] * -1)
                        antiNode = tupleSubtraction(insideDiff, node2)
                        if 0 <= antiNode[0] < bottomRow and 0 <= antiNode[1] < rightCol: antinodePositions.add(antiNode)

    if USE_LOGGING: printMap(antinodePositions)

    return len(antinodePositions)
   
file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = getUniqueAntinodes(input, False)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()
if USE_LOGGING: print('---------PART TWO---------')
startTime = time.time()

solution = getUniqueAntinodes(input, True)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)