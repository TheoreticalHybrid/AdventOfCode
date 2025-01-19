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
    problemData = []
    with open(fileName, 'r') as file:
        for line in file.readlines():
            words = line.strip().split(' ')
            propDict = dict()
            
            for wordIndex in range(2, len(words), 2):
                propDict[words[wordIndex].replace(':', '')] = int(words[wordIndex+1].replace(',', ''))
            
            problemData.append(propDict)

    return problemData

def useMFCSAM(auntData, partTwo):
    targetProperties = [('children', 3), ('cats', 7), ('samoyeds', 2), ('pomeranians', 3), ('akitas', 0), ('vizslas', 0), ('goldfish', 5), ('trees', 3), ('cars', 2), ('perfumes', 1)]
    possibleAunts = list(range(500))

    for tpKey, tpVal in targetProperties:
        auntRemovals = []
        lessThan = tpKey in ['pomeranians', 'goldfish']
        greaterThan = tpKey in ['cats', 'trees']
        for auntNumber in possibleAunts:
            if tpKey in auntData[auntNumber]:
                remove = False
                if partTwo and lessThan:
                    remove = auntData[auntNumber][tpKey] >= tpVal
                elif partTwo and greaterThan:
                    remove = auntData[auntNumber][tpKey] <= tpVal
                else:
                    remove = auntData[auntNumber][tpKey] != tpVal

                if remove: auntRemovals.append(auntNumber)

        possibleAunts = [aunt for aunt in possibleAunts if aunt not in auntRemovals]
        if len(possibleAunts) == 1: return possibleAunts[0] + 1

    return -1

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = useMFCSAM(problemInput, False)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    solution = useMFCSAM(problemInput, True)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)