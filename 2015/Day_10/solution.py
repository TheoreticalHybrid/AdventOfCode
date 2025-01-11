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
        problemData = file.read().strip()

    return problemData

def applySequence(inputValue):
    newSequence = ''

    count = 1
    digit = None
    for c in inputValue:
        if digit is None: digit = c
        else:
            if c == digit: count += 1
            else:
                newSequence += str(count) + digit
                count = 1
                digit = c

    newSequence += str(count) + digit
    return newSequence

def repeatSequence(inputValue, count):
    v = inputValue
    for _ in range(count): v = applySequence(v)
    return v

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = len(repeatSequence(problemInput, 40))

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    solution = len(repeatSequence(problemInput, 50))

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)