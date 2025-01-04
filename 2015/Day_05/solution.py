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
        problemData = file.readlines()

    return problemData

def stringIsNice(candidateString):
    prohibitedStrings = ['ab','cd','pq','xy']
    if any(subStr in candidateString for subStr in prohibitedStrings):
        return False
    elif sum([candidateString.count(v) for v in 'aeiou']) < 3:
        return False
    else:
        for i,l in enumerate(candidateString[0:-1]):
            if l == candidateString[i+1]: return True

    return False

def stringIsNicePartTwo(candidateString):
    repeatedTwoStringCriteria = False
    letterSandwichCriteria = False

    rtsLimit = len(candidateString) - 4
    lsLimit = len(candidateString) - 2
    
    for i,c in enumerate(candidateString[0:-2]):
        if not repeatedTwoStringCriteria and i < rtsLimit:
            twoLetterString = candidateString[i:i+2]
            if twoLetterString in candidateString[i+2:]: repeatedTwoStringCriteria = True

        if not letterSandwichCriteria and i < lsLimit:
            if c == candidateString[i+2]: letterSandwichCriteria = True

        if repeatedTwoStringCriteria and letterSandwichCriteria: return True

    return repeatedTwoStringCriteria and letterSandwichCriteria


if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = len([w for w in problemInput if stringIsNice(w)])

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    #exit()
    print('---------PART TWO---------')
    startTime = time.time()

    solution = len([w for w in problemInput if stringIsNicePartTwo(w)])

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)