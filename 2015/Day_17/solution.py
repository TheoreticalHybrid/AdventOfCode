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
        problemData = [int(l.strip()) for l in file.readlines()]

    problemData.sort(reverse=True)
    return problemData

def getContainerCombinations(amount, containers):
    combos = 0

    for i, container in enumerate(containers):
        if container < amount:
            newAmount = amount - container
            newContainerList = containers[i+1:]
            combos += getContainerCombinations(newAmount, newContainerList)
        elif container == amount: combos += 1

    return combos

def getContainerCombinationLists(amount, containers):
    combos = []

    for i, container in enumerate(containers):
        if container < amount:
            newAmount = amount - container
            newContainerList = containers[i+1:]
            subCombos = getContainerCombinationLists(newAmount, newContainerList)
            combos = combos + [([container] + sc) for sc in subCombos]
        elif container == amount: combos.append([container])

    return combos


if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getContainerCombinations(150, problemInput)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    comboLists = getContainerCombinationLists(150, problemInput)
    minLength = len(min(comboLists, key=len))
    solution = len([c for c in comboLists if len(c) == minLength])

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)