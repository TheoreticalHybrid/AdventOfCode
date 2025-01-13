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
    problemData = dict()
    with open(fileName, 'r') as file:
        for line in file.readlines():
            words = line.strip().split(' ')
            name, speed, endurance, rest = words[0], int(words[3]), int(words[6]), int(words[-2])
            problemData[name] = (speed, endurance, rest)

    return problemData

def getDistanceAfterTime(speed, endurance, rest, time):
    blockDistance = speed * endurance
    blockTime = endurance + rest
    completedBlocks = time // blockTime
    extraTime = time % blockTime

    return (blockDistance * completedBlocks) + (blockDistance if extraTime >= endurance else (speed * (extraTime % endurance)))

def getFastestReindeerDistanceAfterTime(reindeerLookup, time):
    longestDistance = 0

    for r in reindeerLookup:
        d = getDistanceAfterTime(*reindeerLookup[r], time)
        if d > longestDistance: longestDistance = d

    return longestDistance

def getBestReindeerScore(reindeerLookup, time):
    scores = dict()
    for r in reindeerLookup:
        scores[r] = 0

    for s in range(1, time + 1):
        leadReindeerDistance = 0
        leadReindeerNames = []

        for r in reindeerLookup:
            d = getDistanceAfterTime(*reindeerLookup[r], s)

            if d > leadReindeerDistance:
                leadReindeerDistance = d
                leadReindeerNames = [r]
            elif d == leadReindeerDistance:
                leadReindeerNames.append(r)

        for lrn in leadReindeerNames:
            scores[lrn] = scores[lrn] + 1

    return max(scores.values())

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getFastestReindeerDistanceAfterTime(problemInput, 2503)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    solution = getBestReindeerScore(problemInput, 2503)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)