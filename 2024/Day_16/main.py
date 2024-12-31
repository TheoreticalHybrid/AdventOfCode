import time
import os
import re
from typing import Dict

USE_LOGGING = False
USE_DEMO = True

Map = []
Directions = [(-1,0),(0,1),(1,0),(0,-1)] # U, R, D, L

class MapJunction:
    def __init__(self, id, coordinate, isStartPoint, isEndpoint):
        self.Id = id
        self.Coord = coordinate
        self.IsStartPoint = isStartPoint
        self.IsEndpoint = isEndpoint
        self.Paths = dict()
        self.ShortestDistanceToEnd = None
        self.TileCount = 0

    def addPath(self, pathEndCoords, pathLength, pathDirectionIndex, totalTiles):
        if pathEndCoords != self.Id:
            if pathEndCoords not in self.Paths:
                self.Paths[pathEndCoords] = (pathLength, pathDirectionIndex, totalTiles)
        else:
            if pathLength < self.Paths[pathEndCoords][0]:
                self.Paths[pathEndCoords] = (pathLength, pathDirectionIndex, totalTiles)
            elif pathLength == self.Paths[pathEndCoords][0]:
                newTileCount = totalTiles + self.Paths[pathEndCoords][2]
                self.Paths[pathEndCoords] = (pathLength, pathDirectionIndex, newTileCount)

    def removePath(self, pathEndCoords):
        del self.Paths[pathEndCoords]

    def updateShortestRoute(self, distance, directionIndex):
        if self.ShortestDistanceToEnd is None or distance < self.ShortestDistanceToEnd[0]:
            self.ShortestDistanceToEnd = (distance, directionIndex)

def printMap():
    for line in Map:
        print(''.join(line))
    print()

def getInput(fileName):
    global Map
    Map = []

    with open(fileName, 'r') as file:
        Map = [[c for c in line.strip()] for line in file.readlines()]

    startPoint, endPoint = None, None
    for i, line in enumerate(Map):
        if 'S' in line: startPoint = (i, line.index('S'))
        if 'E' in line: endPoint = (i, line.index('E'))

    return (startPoint, endPoint)

def nearestJunctionInDirection(myCoord, directionIndex):
    searching = True
    travelDirection = Directions[directionIndex]
    cx, cy = myCoord
    while searching:
        nextStepX, nextStepY = cx + travelDirection[0], cy + travelDirection[1]
        nextStepChar = Map[nextStepX][nextStepY]
        if nextStepChar == '#': return None
        elif nextStepChar in ('S','E'): return (nextStepX, nextStepY)
        else:
            turnDirections = [Directions[(directionIndex - 1) % 4], Directions[(directionIndex + 1) % 4]]
            for td in turnDirections:
                tdx, tdy = nextStepX + td[0], nextStepY + td[1]
                if Map[tdx][tdy] != '#':
                    return (nextStepX, nextStepY)
                
            cx, cy = nextStepX, nextStepY

def getShortestPath(startingPoint, endPoint):
    startingDirectionIndex = 1

    ForwardNodeDict = dict()

    junctions = [startingPoint]
    discoveredJunctionList = []

    # get all junctions
    while any(junctions):
        junct = junctions.pop(0)
        discoveredJunctionList.append(junct)
        ForwardNodeDict[junct] = set()

        for di in range(4):
            directionalJunction = nearestJunctionInDirection(junct, di)
            if directionalJunction is not None:
                if directionalJunction not in discoveredJunctionList: junctions.append(directionalJunction)
                ForwardNodeDict[junct].add(directionalJunction)

    if USE_LOGGING and False:
        for j in ForwardNodeDict:
            print(f'{j}: {ForwardNodeDict[j]}')

    # Junctions with only one attached junction are just part of a dead end
    while any([k for k in ForwardNodeDict if k not in [startingPoint, endPoint] and len(ForwardNodeDict[k]) == 1]):
        for k in [k for k in ForwardNodeDict if k not in [startingPoint, endPoint] and len(ForwardNodeDict[k]) == 1]:
            if USE_LOGGING: print(f'Removing junction {k}')
            ForwardNodeDict[ForwardNodeDict[k].pop()].remove(k) # remove k from the value of the one juction that k is pointing to (meaning the one junction that k came from)
            del ForwardNodeDict[k]

    # Build the MapJunctionObjects
    jDict: Dict[tuple, MapJunction] = dict()
    jId = 1
    for j in ForwardNodeDict:
        jObj = MapJunction(jId, j, j == startingPoint, j == endPoint)
        jDict[j] = jObj
        jId += 1

    # Build the paths between objects
    for j in ForwardNodeDict:
        jObj = jDict[j]
        for nextJ in ForwardNodeDict[j]:
            distance, dIndex, xDiff, yDiff = 0, 0, j[0] - nextJ[0], j[1] - nextJ[1]
            if xDiff == 0:
                diff = yDiff
                distance = abs(diff)
                dIndex = 3 if diff > 0 else 1
            else:
                diff = xDiff
                distance = abs(diff)
                dIndex = 0 if diff > 0 else 2
            jObj.addPath(nextJ, distance, dIndex, distance)

    # Junctions with only two attached junctions are just turns in a line
    while any([k for k in jDict if k not in [startingPoint, endPoint] and len(jDict[k].Paths) < 3]):
        if USE_LOGGING: print('Starting new loop')
        for k in [k for k in jDict if k not in [startingPoint, endPoint] and len(jDict[k].Paths) < 3]:
            kObj = jDict[k]
            keys = [key for key in kObj.Paths]
            if len(jDict[k].Paths) == 2:
                # for the 2 paths, a and b, replace their path k with the opposite path
                # a -> k of length x and k -> b of length y needs to become a -> b of length x + 1000 + y and b -> a of length x + 1000 + y
                # the extra 1000 is for the turn that would have to happen
                if USE_LOGGING: print(f'Removing junction {k} from {keys}')
                aObj = jDict[keys[0]]
                bObj = jDict[keys[1]]

                # if USE_LOGGING:
                #     for i,l in enumerate(Map):
                #         lCopy = [c for c in l]
                #         for _,kj in [key for key in jDict if key[0] == i]: lCopy[kj] = 'J'
                #         if k[0] == i: lCopy[k[1]] = 'K'
                #         if aObj.Coord[0] == i: lCopy[aObj.Coord[1]] = 'A'
                #         if bObj.Coord[0] == i: lCopy[bObj.Coord[1]] = 'B'
                #         print(f''.join(lCopy))

                kaDist, kaDi, kaTiles = kObj.Paths[keys[0]]
                kbDist, kbDi, kbTiles = kObj.Paths[keys[1]]
                newLength = kaDist + kbDist
                if abs(kaDi - kbDi) != 2: newLength += 1000

                numTiles = kaTiles + kbTiles
                
                aObj.addPath(bObj.Coord, newLength, aObj.Paths[k][1], numTiles)
                bObj.addPath(aObj.Coord, newLength, bObj.Paths[k][1], numTiles)
                del jDict[k]
                aObj.removePath(k)
                bObj.removePath(k)
            else:
                #there's only one, so it's a dead end and needs to be culled
                if USE_LOGGING: print(f'Node {k} has only one path ({keys[0]}), deleting')
                nodeObj = jDict[keys[0]]
                nodeObj.removePath(k)
                del jDict[k]
                

    nodesToExamine = [[endPoint]]

    successfulPaths = []

    while any(nodesToExamine):
        path = nodesToExamine.pop(0)
        node = path[-1]
        sourceNode = jDict[node]
        for n in [snp for snp in sourceNode.Paths if snp not in path]:
            pathNode = jDict[n]
            length, direction = 0, 0
            if node == endPoint:
                length, direction, tiles = pathNode.Paths[node] #length/direction/tiles from node to endpoint
            else:
                # length = shortest length from node object plus length to pathNode,
                # and if the direction from that shortest length is a right turn in relation to node's direction to pathNode, then add 1000
                sdeLength, sdeDir = sourceNode.ShortestDistanceToEnd
                sourceToNodeLength, sourceToNodeDirection, tiles = sourceNode.Paths[n]
                length = sdeLength + sourceToNodeLength
                if abs(sdeDir - sourceToNodeDirection) != 2: length += 1000
                direction = pathNode.Paths[node][1]
            
            if pathNode.ShortestDistanceToEnd is None or length <= pathNode.ShortestDistanceToEnd[0]:
                pathNode.updateShortestRoute(length, direction)

                newPath = [n for n in path]
                newPath.append(n)
                if n == startingPoint:
                    successfulPaths.append(newPath)
                else:
                    nodesToExamine.append(newPath)
    
    shortestDistanceLength, shortestDistanceDirection = jDict[startingPoint].ShortestDistanceToEnd
    numberOfTurns = abs(shortestDistanceDirection - 1) # starts facing right
    shortestDistanceLength += (1000 * numberOfTurns)
    part1Solution = shortestDistanceLength
    
    part2Solution = 0
    pathSections = set()
    pathNodes = set()
    for sp in successfulPaths:
        for i, endNode in enumerate(sp[1:]):
            startNode = sp[i]
            tileCount = jDict[startNode].Paths[endNode][2] - 1
            section = (startNode, endNode)
            if section not in pathSections:
                part2Solution += tileCount
                pathSections.add(section)

                if startNode not in pathNodes:
                    pathNodes.add(startNode)
                    part2Solution += 1

                if endNode not in pathNodes:
                    pathNodes.add(endNode)
                    part2Solution += 1

    return (part1Solution, part2Solution)

exampleFile = 'example.txt'
file = exampleFile if USE_DEMO else 'input1.txt'
problemInput = getInput(file)

startTime = time.time()

solutions = getShortestPath(problemInput[0], problemInput[1])

endtime = time.time()
print('Completion time: ', endtime - startTime)
print(f'Part 1 Solution: ', solutions[0])
print(f'Part 2 Solution: ', solutions[1])
#print ('Part 2 Completion time: ', endtime - startTime)