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
        problemData = [l.strip() for l in file.readlines()]

    return problemData

def setUpLights(instructions, partTwo):
    lightingGrid = [[0 for _ in range(1000)] for _ in range(1000)]

    for i in instructions:
        corner1 = i.split(' ')[-3]
        corner2 = i.split(' ')[-1]
        c1x,c1y = tuple([int(z) for z in corner1.split(',')])
        c2x,c2y = tuple([int(z) for z in corner2.split(',')])

        turnOffCommand = i.startswith('turn off')
        turnOnCommand = i.startswith('turn on')
        toggleCommand = i.startswith('toggle')

        for x in range(c1x, c2x+1):
            for y in range(c1y, c2y+1):
                lgValue = lightingGrid[x][y]
                if turnOffCommand:
                    if lgValue > 0: lightingGrid[x][y] = lgValue - 1
                elif turnOnCommand:
                    if partTwo or lgValue < 1: lightingGrid[x][y] = lgValue + 1
                elif toggleCommand:
                    if partTwo: lightingGrid[x][y] = lgValue + 2
                    else: lightingGrid[x][y] = 0 if lgValue == 1 else 1

    return sum([sum(r) for r in lightingGrid])

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = setUpLights(problemInput, False)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    #exit()
    print('---------PART TWO---------')
    startTime = time.time()

    solution = setUpLights(problemInput, True)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)