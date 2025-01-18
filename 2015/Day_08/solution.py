import sys
import time
from pathlib import Path

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
        problemData = [line.strip() for line in file.readlines()]

    return problemData

def getNumCharacters(inputString):
    internalString = inputString[1:-1] # remove the wrapping ""
    charLen = len(internalString)

    if charLen > 0:            
        matches = re.findall(r'\\[x][0-9a-fA-F]{2}|\\\"|\\\\', internalString)
        for match in matches:
            charLen = charLen - (len(match) - 1)

    return charLen

def getEncodedStringLength(inputString):
    return 2 + sum([2 if c in ['"', '\\'] else 1 for c in inputString])

def getCharacterDiscrepancy(inputValues, partTwo):
    discrepancy = 0

    for value in inputValues:
        if partTwo:
            discrepancy += getEncodedStringLength(value) - len(value)
        else:
            discrepancy += len(value) - getNumCharacters(value)

    return discrepancy

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getCharacterDiscrepancy(problemInput, False)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    solution = getCharacterDiscrepancy(problemInput, True)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)