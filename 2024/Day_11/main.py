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

def witnessChanges(input, blinkCount):
    newList = []

    for i in range(blinkCount):
        iStart = time.time()
        newList = []
        for s in input:
            if s == 0:
                newList.append(1)
            else:
                sn = str(s)
                snl = len(sn)
                if snl % 2 == 0:
                    n1, n2 = int(sn[0:snl//2]), int(sn[snl//2:])
                    newList.append(n1)
                    newList.append(n2)
                else:
                    newList.append(s * 2024)
        input = newList
        iEnd = time.time()
        if USE_LOGGING: print(f'Blink {i} time: {iEnd - iStart}')

    return newList
  
file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

numberOfBlinks = 5 if USE_DEMO else 25
stones = witnessChanges(input, numberOfBlinks)
solution = len(stones)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
if USE_LOGGING: print('---------PART TWO---------')
startTime = time.time()

numberOfBlinks = 75
stones = witnessChanges(input, numberOfBlinks)
solution = len(stones)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)