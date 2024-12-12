import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

Map = []

class GardenRegion:
    def __init__(self, id, name, plotCoordinates):
        self.Name = name
        self.Id = id
        self.PlotCoordinates = sorted(plotCoordinates)

    def addPlot(self, plotCoord):
        self.PlotCoordinates.add(plotCoord)
    
    def getArea(self):
        return len(self.PlotCoordinates)
    
    #Thought Part 2 was going to ask to not double count fences, hence returning the coordinates instead of just a count
    def getPerimeter(self):
        #Representing perimeter lines as pairs of tuples, both indicating the top-left corner of a plot. Direction will always be L->R or U->D
        perimeterLines = set()
        for p in self.PlotCoordinates:
            pi, pj = p
            cards = [(pi-1,pj), (pi,pj+1), (pi+1,pj), (pi,pj-1)] # {U,R,D,L}
            for i,c in enumerate(cards):
                if c not in self.PlotCoordinates:
                    match i:
                        case 0:
                            perimeterLines.add((p, cards[i+1])) #top left to top right
                        case 1:
                            perimeterLines.add((c, (pi+1, pj+1))) #top right to lower right
                        case 2:
                            perimeterLines.add((c, (pi+1, pj+1))) #lower left to lower right
                        case 3:
                            perimeterLines.add((p, cards[i-1])) #top left to lower left

        return perimeterLines

    def getSidesCount(self):
        perimeter = sorted(list(self.getPerimeter()))
        hSides = dict()
        vSides = dict()
        for p in perimeter:
            p1, p2 = p
            p1i, p1j = p1
            p2i, p2j = p2
            horizontal = p1i == p2i
            if horizontal:
                if p1i not in hSides:
                    hSides[p1i] = [(p1j, p2j)]
                else:
                    newLine = True
                    for index, l in enumerate(hSides[p1i]):
                        jMin, jMax = l
                        if p1j == jMax:
                            #check if the fence is a north or south bordering fence and compare to existing line
                            pNorthBorder = p1 in self.PlotCoordinates
                            lNorthBorder = (p1i, jMin) in self.PlotCoordinates
                            if pNorthBorder == lNorthBorder:
                                hSides[p1i][index] = (jMin, p2j)
                                newLine = False

                    if newLine: hSides[p1i].append((p1j, p2j))
            else:
                if p1j not in vSides:
                    vSides[p1j] = [(p1i, p2i)]
                else:
                    newLine = True
                    for index, l in enumerate(vSides[p1j]):
                        iMin, iMax = l
                        if p1i == iMax:
                            pWestBorder = p1 in self.PlotCoordinates
                            lWestBorder = (iMin, p1j) in self.PlotCoordinates
                            if pWestBorder == lWestBorder:
                                vSides[p1j][index] = (iMin, p2i)
                                newLine = False

                    if newLine: vSides[p1j].append((p1i, p2i))

        sideCount = 0
        if USE_LOGGING: print(f'Region {self.Name}')
        if USE_LOGGING: print('Horizontal Sides')
        for i in hSides:
            if USE_LOGGING: print(f'Row {i}: {hSides[i]}')
            sideCount += len(hSides[i])
        
        if USE_LOGGING: print()
        if USE_LOGGING: print('Vertical Sides')
        
        for j in vSides:
            if USE_LOGGING: print(f'Column {j}: {vSides[j]}')
            sideCount += len(vSides[j])

        if USE_LOGGING: print()

        return sideCount

    def printCoords(self):
        print(f'Plots: {sorted(self.PlotCoordinates)}')
        print()
    
    def __repr__(self):
        return f'Region {self.Id}: {self.Name} ({len(self.PlotCoordinates)})'

def buildRegion(startingCoords, id):
    ci, cj = startingCoords
    regionName = Map[ci][cj]
    bottomRow, rightColumn = len(Map), len(Map[0])

    plots = set()
    unMappedPlots = {startingCoords}
    while any(unMappedPlots):
        pi, pj = unMappedPlots.pop()
        cards = {(pi-1,pj), (pi,pj+1), (pi+1,pj), (pi,pj-1)} # {U,R,D,L}
        for c in cards:
            ci, cj = c
            if 0 <= ci < bottomRow and 0 <= cj < rightColumn and Map[ci][cj] == regionName and c not in plots:
                unMappedPlots.add(c)
        plots.add((pi, pj))

    return GardenRegion(id, regionName, plots)

def getInput(fileName):
    global Map
    
    with open(fileName, 'r') as file:
        Map = [[c for c in line.strip()] for line in file.readlines()]

    regions: list[GardenRegion] = []
    plotId = 1
    
    for i, line in enumerate(Map):
        for j, c in enumerate(line):
            plotCoord = (i,j)

            if not any([r for r in regions if r.Name == c and plotCoord in r.PlotCoordinates]):
                regions.append(buildRegion(plotCoord, plotId))
                plotId += 1

    if USE_LOGGING:
        for r in regions:
            print(r)
            r.printCoords()

    return regions

def getTotalFencePrice(regions: list[GardenRegion], partTwo):
    totalPrice = 0
    for r in regions:
        fenceUnit = r.getSidesCount() if partTwo else len(r.getPerimeter())
        if USE_LOGGING: print(f'Region {r.Name} has {fenceUnit} {'sides' if partTwo else 'perimeter'}')
        totalPrice += fenceUnit * r.getArea()

    return totalPrice

exampleFile = 'example2.txt'
file = exampleFile if USE_DEMO else 'input1.txt'
input = getInput(file)
#exit()

startTime = time.time()

solution = getTotalFencePrice(input, False)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
print('---------PART TWO---------')
startTime = time.time()

solution = getTotalFencePrice(input, True)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)