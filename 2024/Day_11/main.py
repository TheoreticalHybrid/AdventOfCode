import time
import os
import re

USE_LOGGING = True
USE_DEMO = False

def getInput(fileName):
    input = set()
    
    with open(fileName, 'r') as file:
        input = [int(n) for n in file.read().strip().split()]
            
    if USE_LOGGING:
        print(input)

    return input

def stoneChange(stoneValue):
    newValue = []
    if stoneValue == 0:
        newValue = [1]
    else:
            sn = str(stoneValue)
            snl = len(sn)
            if snl % 2 == 0:
                newValue = [int(sn[0:snl//2]), int(sn[snl//2:])]
            else:
                newValue = [stoneValue * 2024]

    return newValue

def witnessChanges4(input, blinkCount):
    calcDict = dict()

    count = 0
    for value in input:
        values = [(value, blinkCount)]
        queueLength = 0
        while any(values):
            stoneValue, remainingBlinks = values.pop(0)
            count += 1

            foundNewValues = False
            for i in range(remainingBlinks):                
                newValue = None
                if stoneValue in calcDict:
                    newValue = calcDict[stoneValue]
                else:
                    newValue = stoneChange(stoneValue)
                    calcDict[stoneValue] = newValue
                    foundNewValues = True
                    
                stoneValue = newValue[0]
                if len(newValue) > 1: values.append((newValue[1], remainingBlinks - (i + 1)))
            
            if USE_LOGGING: 
                currentLength = len(values)
                threshold = 500
                if currentLength > queueLength + threshold or currentLength < queueLength - threshold:
                    print(f'NewValues: {foundNewValues} - Queue Length - {currentLength}                  ', end='\r')
                    queueLength = currentLength

    return count

def witnessChanges3(input, blinkCount):
    calcDict = dict()

    for value in input:
        testValues = {value}
        visitedValues = set()
        for i in range(blinkCount):
            if not any(testValues):
                print(f'{value} has no more unique values to test at blink {i}')
                break
            iStart = time.time()
            iValues = set(testValues)
            testValues = set()
            for s in iValues:
                if s in visitedValues:
                    print(f'{value} after blink {i} found a repeat value ({s})')
                else:
                    newValue = stoneChange(s)

                    if USE_LOGGING: print(f'Blink {i}: {s} -> {newValue}')
                    calcDict[s] = newValue
                    testValues.update(newValue)
                    visitedValues.add(s)
            
            iEnd = time.time()
            print(f'Blink {i} time: {iEnd - iStart}')

    stoneCount = 0
    print(f'Counting Now')

    for value in input:
        stones = [value]
        stoneCount += 1
        for i in range(blinkCount):
            subStones = []
            for stone in stones:
                subStones = subStones + calcDict[stone]
            
            stoneCount += len(subStones)
            stones = subStones

    return stoneCount

def loopTest(value):
    loop = [value]

    
  
file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

numberOfBlinks = 5 if USE_DEMO else 25
solution = witnessChanges4(input, numberOfBlinks)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
print('---------PART TWO---------')
startTime = time.time()

numberOfBlinks = 75
solution = witnessChanges4(input, numberOfBlinks)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)