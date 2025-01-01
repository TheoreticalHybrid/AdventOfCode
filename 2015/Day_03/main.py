import sys
import time
from pathlib import Path

from functools import reduce
from operator import mul

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
        problemData = list(file.read())

    return problemData

def getHouseCount(problemInput):
    x,y = 0,0
    visitedHouses = set()
    visitedHouses.add((x,y))

    for dir in problemInput:
        match dir:
            case '<':
                x = x-1
            case '>':
                x = x+1
            case '^':
                y = y-1
            case 'v':
                y = y+1
        
        visitedHouses.add((x,y))

    return len(visitedHouses)

def getRoboHouseCount(problemInput):
    x,y = 0,0
    rx,ry = 0,0
    visitedHouses = set()
    visitedHouses.add((x,y))
    santasTurn = True

    for dir in problemInput:
        myX, myY = (x,y) if santasTurn else (rx,ry)
        match dir:
            case '<':
                myX = myX-1
            case '>':
                myX = myX+1
            case '^':
                myY = myY-1
            case 'v':
                myY = myY+1
        
        visitedHouses.add((myX,myY))
        if santasTurn: x,y = myX,myY
        else: rx,ry = myX,myY
        santasTurn = not santasTurn

    return len(visitedHouses)

exampleFile = 'example2.txt'
file = exampleFile if USE_DEMO else 'input.txt'
problemInput = getProblemInput(file)
#exit()

startTime = time.time()

solution = getHouseCount(problemInput)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
print('---------PART TWO---------')
startTime = time.time()

solution = getRoboHouseCount(problemInput)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)