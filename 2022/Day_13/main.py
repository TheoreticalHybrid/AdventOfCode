from enum import Enum
import getopt
import sys
import time
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = True

def getInput(fileName):
    global GRID_HEIGHT
    global GRID_WIDTH
    global PointGrid

    file = open(fileName, 'r')
    
    input = [pp.split("\n") for pp in file.read().split("\n\n")]

    if USE_LOGGING: print(input)

    return input

def comparePackets(leftPacket, rightPacket):
    splitCharacter, lBracket, rBracket = ",", "[", "]"
    
    lPacket = [x.strip() for x in leftPacket.split(splitCharacter)]
    rPacket = [x.strip() for x in rightPacket.split(splitCharacter)]

    # if USE_LOGGING:
    #     print(lPacket)
    #     print(rPacket)
    #     print()

    listStack = [] #might not actually be necessary to keep track of how deep the lists are

    for i in range(max(len(lPacket), len(rPacket))):
        if i == len(lPacket): return False #right packet was shorter
        if i == len(rPacket): return True #left packet was shorter

        l = lPacket[i]
        r = rPacket[i]

        while (len(l) > 0 or len(r) > 0):
            if USE_LOGGING: print(f'\tComparing {l} and {r}')

            if len(l) == 0: return True
            elif len(r) == 0: return False

            if l.isnumeric() and r.isnumeric():
                if l == r: break
                else: return int(l) < int(r)

            if l[0] == lBracket and r[0] == lBracket:
                listStack.append(lBracket)
                l = l[1:]
                r = r[1:]
                continue

            if l[0] == lBracket:
                if r[0] == rBracket: return False
                if r[0] != lBracket: 
                    r = f'[{r}]'
                    continue
            elif r[0] == lBracket:
                if l[0] == rBracket: return True
                if l[0] != lBracket: #redundant check, but whatever
                    l = f'[{l}]'
                    continue
            
            if l[0] == rBracket or r[0] == rBracket:
                if l[0] == r[0]:
                    listStack.pop()
                    l = l[1:]
                    r = r[1:]
                    continue
                else:
                    return l[0] == rBracket


            if l[-1] == rBracket and r[-1] == rBracket:
                listStack.pop()
                l = l[:-1]
                r = r[:-1]
                continue
            elif l[-1] == rBracket:
                return int(l[:l.index(rBracket)]) <= int(r)
            elif r[-1] == rBracket:
                return int(l) < int(r[:r.index(rBracket)])

    return True

def getCorrectPackets(input):
    correctIndexes = []
    for i, packetPair in enumerate(input):
        allG = comparePackets(packetPair[0], packetPair[1])
        
        if USE_LOGGING:
            keyword = 'CORRECT' if allG else 'WRONG'
            print(f'PACKETS ARE IN THE {keyword} ORDER')

        if allG: correctIndexes.append(i)

    return correctIndexes

def main(argv):
    global USE_DEMO
    global USE_LOGGING
    
    solution = 0

    opts, args = getopt.getopt(argv, "el")
    for opt, arg in opts:
        match opt:
            case "-e":
                USE_DEMO = True
            case "-l":
                USE_LOGGING = True
    
    #USE_DEMO = True
    USE_LOGGING = True

    startTime = time.perf_counter()

    file = 'example.txt' if USE_DEMO else 'input1.txt'

    input = getInput(file)
    correctPackets = getCorrectPackets(input)

    if PART_ONE:
        if USE_LOGGING: print(correctPackets)
        solution = sum(correctPackets) + len(correctPackets)

    endtime = time.perf_counter()

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])