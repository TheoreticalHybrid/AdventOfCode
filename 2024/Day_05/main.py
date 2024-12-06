import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

Rules = dict()

def getInput(fileName):
    global Rules
    file = open(fileName, 'r')
    input = []

    for line in file.readlines():
        line = line.strip()
        if '|' in line:
            key, value = tuple(int(v) for v in line.split('|'))
            valueSet = Rules[key] if key in Rules else set()
            valueSet.add(value)
            Rules[key] = valueSet
        elif ',' in line:
            input.append([int(p) for p in line.split(',')])

    if USE_LOGGING: 
        print(Rules)
        print(input)

    return input

def validateUpdate(update):
    reversedUpdate = update[::-1]
    for i, page in enumerate(reversedUpdate[:-1]):
        if page in Rules and not Rules[page].isdisjoint(set(reversedUpdate[i+1:])):
            if USE_LOGGING: print(f'INVALID: {update} - CAUSE: {page}\n')
            return False

    if USE_LOGGING: print(f'ALL GOOD: {update}')
    return True

def updateCorrection(update):
    newUpdate = []

    reversedUpdate = update[::-1]
    correct = False
    while not correct:
        for i, page in enumerate(reversedUpdate[:-1]):
            remainder = reversedUpdate[i+1:]
            if page in Rules and not Rules[page].isdisjoint(set(remainder)):
                #find index of correct place
                newIndex = None
                for j, x in enumerate(remainder):
                    remainderPlus = remainder[j+1:]
                    if Rules[page].isdisjoint(set(remainderPlus)):
                        newIndex = i+j+2
                        if USE_LOGGING: print(f'Found new index for {page} at {newIndex}')
                        break

                #insert at that index
                reversedUpdate.insert(newIndex, page)

                #remove from my index
                reversedUpdate.pop(i)

                break

        correct = validateUpdate(reversedUpdate[::-1])

    newUpdate = reversedUpdate[::-1]

    return newUpdate

def findValidMidSum(input, partTwo):
    sum = 0

    for update in input:
        middleIndex = int((len(update) - 1) / 2)
        if validateUpdate(update):
            if not partTwo:
                middleNumber = update[middleIndex]
                if USE_LOGGING: print(f'Adding {middleNumber}\n')
                sum += middleNumber
        elif partTwo:
            correctedUpdate = updateCorrection(update)
            middleNumber = correctedUpdate[middleIndex]
            if USE_LOGGING: print(f'Adding {middleNumber}\n')
            sum += middleNumber

    return sum

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = findValidMidSum(input, False)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()
if USE_LOGGING: print('---------PART TWO---------')
startTime = time.time()

solution = findValidMidSum(input, True)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)