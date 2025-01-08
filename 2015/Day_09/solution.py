import sys
import time
from pathlib import Path

options = [opt for opt in sys.argv[1:] if opt.startswith("-")]
arguments = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

USE_LOGGING = '-v' in options
USE_DEMO = '-d' in options

if '-f' in options:
    #Ask for user input to keep going
    userInput = input("File: ")
    my_file = Path(userInput)
    if not my_file.is_file():
        raise SystemExit(f"File {userInput} is not found")

def getProblemInput(fileName):
    problemData = ''
    with open(fileName, 'r') as file:
        problemData = file.readlines()

    return problemData

DistanceLookup = dict()

def processMapData(mapData):
    locations = set()

    for route in mapData:
        r, l = route.split(' = ')
        a, b = r.split(' to ')
        locations.add(a)
        locations.add(b)
        
        if a not in DistanceLookup: DistanceLookup[a] = dict()
        if b not in DistanceLookup: DistanceLookup[b] = dict()

        DistanceLookup[a][b] = int(l)
        DistanceLookup[b][a] = int(l)

    return locations

def getDistance(a, b):
    if a not in DistanceLookup:
        raise KeyError(f'Location {a} not found')
    elif b not in DistanceLookup[a]:
        raise KeyError(f'Location {b} not found as a route from {a}')
    else:
        return DistanceLookup[a][b]
    
def getBestRoutes(locations, takeShortest):
    bestDistances = []
    bestDistance = 0
    bestRoute = []
    if len(locations) == 1:
        bestRoute = list(locations)
        bestDistances.append((bestRoute, bestDistance))
        return bestDistances
    else:
        for l in locations:
            subset = set(locations)
            subset.remove(l)

            try:
                for br in getBestRoutes(subset, takeShortest):
                    r,d = br
                    try:
                        locationDist = getDistance(l, r[0])
                        routeDist = d + locationDist
                        r.insert(0,l)

                        if bestDistance == 0 or (routeDist < bestDistance if takeShortest else routeDist > bestDistance):
                            bestDistance = routeDist
                            bestRoute = r
                            bestDistances = [(bestRoute, bestDistance)]
                        elif routeDist == bestDistance:
                            bestDistances.append((r,routeDist))
                    except KeyError:
                        pass
            except ValueError:
                pass

        if bestDistance == 0: raise ValueError(f'Unfinishable Route {locations}')
        return bestDistances

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    locations = processMapData(problemInput)
    shortestRoutes = getBestRoutes(locations, True)
    solution = shortestRoutes[0][1]

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    longestRoutes = getBestRoutes(locations, False)
    solution = longestRoutes[0][1]

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)