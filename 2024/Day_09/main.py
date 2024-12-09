import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

def getInput(fileName):    
    input = ''
    
    with open(fileName, 'r') as file:
        input = file.read().strip()

    if USE_LOGGING:
        print(len(input))

    return input

def getFragmentationChecksum(input):
    sum = 0

    inputLength = len(input)
    currentFileId, lastFileId = 0, int((inputLength / 2) - 1 if inputLength % 2 == 0 else (inputLength - 1) / 2)
    tailValues = []
    multiplier = 0
    i, eolPointer = 0, inputLength + 1 #setting eol pointer ABOVE the length is because the first time it's used it's reduced by two to start
    while i < eolPointer:
        freeSpace = i % 2 > 0
        numBlocks = int(input[i])
        nextMultiplier = multiplier + numBlocks

        if freeSpace:
            for j in range(multiplier, nextMultiplier):
                if not any(tailValues):
                    eolPointer = eolPointer - 2
                    if eolPointer < i: break
                    tailValues = [lastFileId] * int(input[eolPointer])
                    lastFileId = lastFileId - 1

                mVal = tailValues.pop()
                if USE_LOGGING: print(f'Adding: {j} * {mVal}')
                sum += j * mVal

        else:
            for j in range(multiplier, nextMultiplier):
                if USE_LOGGING: print(f'Adding: {j} * {currentFileId}')
                sum += j * currentFileId
            
            currentFileId += 1
        
        multiplier = nextMultiplier
        i += 1

    while any(tailValues):
        if USE_LOGGING: print(f'Leftover values - {tailValues[0]}')
        sum += multiplier * tailValues.pop()
        multiplier += 1

    return sum

def getWholeFileChecksum(input):
    sum = 0

    #testString = ''

    inputLength = len(input)
    currentFileId, lastFileId = 0, int((inputLength / 2) - 1 if inputLength % 2 == 0 else (inputLength - 1) / 2)
    shiftedIndexes = set()
    multiplier = 0
    i, eolPointer = 0, inputLength - 1
    while i < inputLength:        
        freeSpace = i % 2 > 0
        numBlocks = int(input[i])
        nextMultiplier = multiplier + numBlocks

        if freeSpace:
            freeSpaceInBlock = numBlocks

            while freeSpaceInBlock > 0:
                highFileId = lastFileId
                outOfOptions = True
                for j in range(eolPointer, i, -2):
                    if j not in shiftedIndexes:
                        highFileBlockNum = int(input[j])
                        if 0 < highFileBlockNum <= freeSpaceInBlock:
                            subMultiplier = multiplier + highFileBlockNum
                            for k in range(multiplier, subMultiplier):
                                if USE_LOGGING: print(f'Adding: {k} * {highFileId}')
                                sum += k * highFileId
                                #testString += str(highFileId)

                            freeSpaceInBlock = freeSpaceInBlock - highFileBlockNum
                            shiftedIndexes.add(j)

                            if j == eolPointer:
                                while eolPointer in shiftedIndexes:
                                    eolPointer = eolPointer - 2
                                    lastFileId = lastFileId - 1

                            multiplier = subMultiplier
                            outOfOptions = False

                            break
                    
                    highFileId = highFileId - 1

                if outOfOptions:
                    while freeSpaceInBlock > 0:
                        freeSpaceInBlock = freeSpaceInBlock - 1
                        #testString += '.'

            #if USE_LOGGING: print(testString)

        else:
            if i in shiftedIndexes:
                pass
                #for j in range(numBlocks): 
                    #testString += '.'
            else:
                for j in range(multiplier, nextMultiplier):
                    if USE_LOGGING: print(f'Adding: {j} * {currentFileId}')
                    sum += j * currentFileId
                    #testString += str(currentFileId)
            
            currentFileId += 1
            #if USE_LOGGING: print(testString)
        
        multiplier = nextMultiplier
        i += 1

    return sum
   
file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = getFragmentationChecksum(input)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()
if USE_LOGGING: print('---------PART TWO---------')
startTime = time.time()

solution = getWholeFileChecksum(input)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)