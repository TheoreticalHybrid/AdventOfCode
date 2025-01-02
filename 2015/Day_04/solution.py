import sys
import time
from pathlib import Path

import hashlib

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

def getmd5Hash(hashString):
    hashValue = hashlib.md5(hashString.encode())
    return hashValue.hexdigest()

def getLowestHashNumber(problemInput, startingValue):
    hashNum = 0

    searching = True
    while searching:
        hashStr = problemInput + str(hashNum)
        hashOutput = getmd5Hash(hashStr)
        if hashOutput.startswith(startingValue): return hashNum
        hashNum += 1

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getLowestHashNumber(problemInput, '00000')

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    #exit()
    print('---------PART TWO---------')
    startTime = time.time()

    solution = getLowestHashNumber(problemInput, '000000')

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)