import sys
import time
from pathlib import Path

import itertools

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
        for line in file.readlines():
            words = line.strip()[0:-1].split(' ')
            value = int(words[3]) * (-1 if words[2] == 'lose' else 1)
            problemData.append((words[0], words[-1], value))

    return problemData

def buildHappinessDictionary(happinessPotentials, partTwo):
    happinessLookup = dict()

    myName = 'me'
    if partTwo: happinessLookup[myName] = dict()

    for person, neighbor, happiness in happinessPotentials:
         if person not in happinessLookup: 
            happinessLookup[person] = dict()
            
            if partTwo:
                happinessLookup[person][myName] = 0
                happinessLookup[myName][person] = 0

         happinessLookup[person][neighbor] = happiness

    return happinessLookup

def getHappinessValue(seatingList, happyLookup):
    happinessSum = 0

    l = len(seatingList)
    for i,person in enumerate(seatingList):
        happinessSum += happyLookup[person][seatingList[i-1]] + happyLookup[person][seatingList[(i+1)%l]]

    return happinessSum

def getOptimalSeatingValue(happinessPotentials, partTwo):
    happinessLookup = buildHappinessDictionary(happinessPotentials, partTwo)

    bestHappinessValue = 0
    # iterate over every permutation and determine best happiness value
    for seatingOption in itertools.permutations(list(happinessLookup.keys())):
        hVal = getHappinessValue(seatingOption, happinessLookup)
        if hVal > bestHappinessValue:
            bestHappinessValue = hVal

    return bestHappinessValue

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getOptimalSeatingValue(problemInput, False)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    solution = getOptimalSeatingValue(problemInput, True)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)