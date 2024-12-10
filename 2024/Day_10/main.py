import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

Map = []

def getInput(fileName):
    global Map
    input = set()
    
    with open(fileName, 'r') as file:
        Map = [[int(c) for c in line.strip()] for line in file.readlines()]

    for i, line in enumerate(Map):
        for j in [z for z, x in enumerate(line) if x == 0]:
            input.add((i,j))
            
    if USE_LOGGING:
        for line in Map:
            print(f'{''.join([str(c) for c in line])}')
        print()
        print(input)

    return input

#Builds a new map where every cell is the number of unique paths to a 9
def buildRatingMap():    
    bottomEdge, rightEdge = len(Map), len(Map[0])
    ratings = [[0 for i in range(rightEdge)] for j in range(bottomEdge)]

    #Find the 9's and their step downs
    steps = set() # ((higher step), (lower step))
    for i, line in enumerate(Map):
        for j in [z for z, x in enumerate(line) if x == 9]:
            ratings[i][j] = 1
            cards = {(i-1,j), (i,j+1), (i+1,j), (i,j-1)} # {U,R,D,L}
            for c in cards:
                stepI, stepJ = c
                if 0 <= stepI < bottomEdge and 0 <= stepJ < rightEdge:
                    stepElevation = Map[stepI][stepJ]
                    if stepElevation == 8: steps.add(((i,j),c))

    while any(steps):
        newSteps = set() # for the next set of steps down
        visitedSteps = set()
        for s in steps:
            peak, step = s
            pi, pj = peak
            si, sj = step
            
            #Increase the step's rating
            ratings[si][sj] += ratings[pi][pj]
            elevation = Map[si][sj]

            #get the next set of steps down from this step, but only if it hasn't been done yet and our current elevation is above 0
            if step not in visitedSteps and elevation > 0:
                cards = {(si-1,sj), (si,sj+1), (si+1,sj), (si,sj-1)} # {U,R,D,L}
                for c in cards:
                    stepI, stepJ = c
                    if 0 <= stepI < bottomEdge and 0 <= stepJ < rightEdge:
                        stepElevation = Map[stepI][stepJ]
                        if stepElevation == elevation - 1: newSteps.add((step,c))
                visitedSteps.add(step)

        steps = newSteps

    if USE_LOGGING:
        for line in ratings:
            print(line)

    return ratings

#Builds a new map where every cell is the number of 9's reachable from that cell
def buildScoreMap():
    bottomEdge, rightEdge = len(Map), len(Map[0])
    scores = [[0 for i in range(rightEdge)] for j in range(bottomEdge)]

    #Find the 9's
    peaks = set()
    for i, line in enumerate(Map):
        for j in [z for z, x in enumerate(line) if x == 9]:
            peaks.add((i,j))

    for peak in peaks:
        pi, pj = peak
        elevation = Map[pi][pj]

        steps = set()
        cards = {(pi-1,pj), (pi,pj+1), (pi+1,pj), (pi,pj-1)} # {U,R,D,L}
        for c in cards:
            stepI, stepJ = c
            if 0 <= stepI < bottomEdge and 0 <= stepJ < rightEdge:
                stepElevation = Map[stepI][stepJ]
                if stepElevation == elevation - 1: steps.add(c)

        visitedSteps = set()

        while any(steps):
            s = steps.pop()
            if s in visitedSteps: continue
            visitedSteps.add(s)
            si, sj = s

            elevation = Map[si][sj]
            scores[si][sj] += 1

            if elevation == 0: continue

            cards = {(si-1,sj), (si,sj+1), (si+1,sj), (si,sj-1)} # {U,R,D,L}
            for c in cards:
                stepI, stepJ = c
                if 0 <= stepI < bottomEdge and 0 <= stepJ < rightEdge:
                    stepElevation = Map[stepI][stepJ]
                    if stepElevation == elevation - 1: steps.add(c)

    if USE_LOGGING:
        for line in scores: print(line)

    return scores

def getTrailheadSum(trailheads, partTwo):
    sum = 0

    solutionMap = buildRatingMap() if partTwo else buildScoreMap()

    for th in trailheads:
        sum += solutionMap[th[0]][th[1]]

    return sum
   
file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = getTrailheadSum(input, False)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
if USE_LOGGING: print('---------PART TWO---------')
startTime = time.time()

solution = getTrailheadSum(input, True)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)