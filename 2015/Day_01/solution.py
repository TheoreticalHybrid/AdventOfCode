import sys
import time
from pathlib import Path
import os
import re

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
        problemData = file.read()

    return problemData

def getEndingFloor(problemString):
    return problemString.count('(') - problemString.count(')')

def getFirstBasementIndex(problemString):
    thisFloor = 0

    for i,c in enumerate(problemString):
        thisFloor = thisFloor + (1 if c == '(' else -1)
        if thisFloor == -1:
            return i + 1


if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getEndingFloor(problemInput)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    #exit()
    print('---------PART TWO---------')
    startTime = time.time()

    solution = getFirstBasementIndex(problemInput)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)