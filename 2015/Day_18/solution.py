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
    problemData = []
    with open(fileName, 'r') as file:
        problemData = [[1 if c=='#' else 0 for c in l.strip()] for l in file.readlines()]

    return problemData

def animateGrid(startingGrid, numberOfSteps, partTwo):
    myGrid = startingGrid
    gridFarEdgeIndex = len(startingGrid) - 1
    
    corners = [(0,0), (0, gridFarEdgeIndex), (gridFarEdgeIndex, 0), (gridFarEdgeIndex, gridFarEdgeIndex)]
    if partTwo:
        for ci,cj in corners:
            myGrid[ci][cj] = 1

    for _ in range(numberOfSteps):
        nextLightingGrid = [[c for c in r] for r in myGrid]

        for i,row in enumerate(myGrid):
            for j,light in enumerate(row):

                thisLightOn = light == 1
                onNeighbors = 0
                
                if not partTwo or (i,j) not in corners:
                    for x in range(max(j-1,0), min(j+1,len(row)-1)+1):
                        for y in range(max(i-1,0), min(i+1, gridFarEdgeIndex)+1):
                            if (i,j) != (y,x) and myGrid[y][x] == 1: onNeighbors += 1

                    if thisLightOn:
                        if onNeighbors not in [2,3]: 
                            nextLightingGrid[i][j] = 0
                    else:
                        if onNeighbors == 3: 
                            nextLightingGrid[i][j] = 1

        myGrid = nextLightingGrid

    return myGrid

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    finalGridState = animateGrid(problemInput, 100, False)
    solution = sum([sum(r) for r in finalGridState])

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    finalGridState = animateGrid(problemInput, 100, True)
    solution = sum([sum(r) for r in finalGridState])

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)