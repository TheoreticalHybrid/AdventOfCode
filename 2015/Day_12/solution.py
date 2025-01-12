import sys
import time
from pathlib import Path

import json

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
        problemData = file.read().strip()

    return problemData

def getSumOfNumbers(inputValue):
    sum = 0
    numString = ''
    negated = False

    for c in inputValue:
        if c.isdigit(): numString += c # we found a digit, add it to the string
        elif c == '-' and not numString: negated = True # we found a dash and there isn't yet a number being built, we might be starting a negative number
        elif numString: # we found a non-numeric character and numString has been populated, therefore we reached the end of a number
            sum += int(numString) * (-1 if negated else 1)
            numString = ''
            negated = False
        elif negated: negated = False # we found a non-numeric character and previously found a dash that wasn't used as part of a number, so it wasn't a negation symbol

    return sum

def getSumOfArray(arrayValue):
    sum = 0

    for av in arrayValue:
        match av:
            case int(): sum += av
            case list(): sum += getSumOfArray(av)
            case dict(): sum += getSumOfObject(av)

    return sum

def getSumOfObject(objectValue):
    sum = 0

    for value in objectValue.values():
        match value:
            case str():
                if value.lower() == 'red': return 0
            case int(): sum += value
            case list(): sum += getSumOfArray(value)
            case dict(): sum += getSumOfObject(value)

    return sum

def getSumOfNumbersIgnoringRedObjects(inputValue):
    jsonInput = json.loads(inputValue)
    return getSumOfArray(jsonInput) if type(jsonInput) is list else getSumOfObject(jsonInput)

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getSumOfNumbers(problemInput)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    # I could probably just write a method that finds the sum of all red objects and then subtract that from the part 1 solution,
    # but for the unit tests I felt like I should probably just write a new method that does the whole thing
    solution = getSumOfNumbersIgnoringRedObjects(problemInput)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)