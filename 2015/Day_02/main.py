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
        problemData = [[int(d) for d in l.split('x')] for l in file.readlines()]

    return problemData

def getWrappingPaperOrder(problemInput):
    amount = 0

    for present in problemInput:
        length, width, height = present
        side1, side2, side3 = length * width, length * height, width * height
        smallestSide = min(side1, side2, side3)
        amount += (2*(side1 + side2 + side3) + smallestSide)

    return amount

def getRibbonOrder(problemInput):
    amount = 0

    for present in problemInput:
        present.sort()
        amount += (2*(present[0]+present[1]) + reduce(mul, present, 1))

    return amount

exampleFile = 'example2.txt'
file = exampleFile if USE_DEMO else 'input.txt'
problemInput = getProblemInput(file)
#exit()

startTime = time.time()

solution = getWrappingPaperOrder(problemInput)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
print('---------PART TWO---------')
startTime = time.time()

solution = getRibbonOrder(problemInput)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)