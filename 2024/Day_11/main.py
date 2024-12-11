import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

StoneDict = dict()

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
            newValue = [int(sn[0:snl//2]), int(sn[snl//2:])] if snl % 2 == 0 else [stoneValue * 2024]
            
    return newValue

def getStoneBlinkValue(stoneValue, blinkCount):
    if stoneValue not in StoneDict:
        StoneDict[stoneValue] = dict()

    if blinkCount not in StoneDict[stoneValue]:
        stoneCount = 0
        
        if blinkCount == 0:
            stoneCount = 1
        else:
            blinkOnceValue = stoneChange(stoneValue)
            stoneCount = 0
            for bv in blinkOnceValue: stoneCount += getStoneBlinkValue(bv, blinkCount - 1)
        
        StoneDict[stoneValue][blinkCount] = stoneCount
        return stoneCount
    else:
        return StoneDict[stoneValue][blinkCount]    

def witnessChanges5(input, blinkCount):
    global StoneDict

    total = 0
    for value in input:
        total += getStoneBlinkValue(value, blinkCount)

    return total
  
file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

numberOfBlinks = 6 if USE_DEMO else 25
solution = witnessChanges5(input, numberOfBlinks)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
print('---------PART TWO---------')
startTime = time.time()

numberOfBlinks = 75
solution = witnessChanges5(input, numberOfBlinks)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)