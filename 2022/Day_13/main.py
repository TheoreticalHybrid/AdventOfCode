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

def convertPacket(packet):
    splitCharacter, lBracket, rBracket = ",", "[", "]"
    packet = packet[1:-1].strip() #cut off the end brackets
    packetList = []

    while len(packet) > 0:
        if packet[0] == lBracket:            
            #find matching rBracket
            listEndIndex = packet.find(rBracket) + 1
            if listEndIndex < 0: raise Exception("Closing bracket not found")
            listItem = packet[:listEndIndex]
            internalList = convertPacket(listItem)
            packetList.append(internalList)
            packet = packet[listEndIndex:].strip()
        else:
            commaIndex = packet.find(splitCharacter)

            if commaIndex == 0:
                packet = packet[1:]
                continue
            
            if commaIndex < 0 and not packet.isnumeric(): raise Exception("Some weird shit goin on")

            n = int(packet) if commaIndex < 0 else int(packet[:commaIndex])
            packetList.append(n)
            packet = packet[commaIndex+1:].strip() if commaIndex >= 0 else ""

    return packetList


def comparePackets2(leftPacket, rightPacket):
    lPacket = convertPacket(leftPacket)
    rPacket = convertPacket(rightPacket)

    return True

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
        if i == len(lPacket): 
            if USE_LOGGING: print(f'\t\tRight packet was shorter')
            return False #right packet was shorter
        if i == len(rPacket):
            if USE_LOGGING: print(f'\t\tLeft packet was shorter')
            return True #left packet was shorter

        l = lPacket[i]
        r = rPacket[i]

        while (len(l) > 0 or len(r) > 0):
            if USE_LOGGING: print(f'\tComparing {l} and {r}')

            if len(l) == 0: 
                if USE_LOGGING: print(f'\t\tLeft chunk ran out')
                return True
            elif len(r) == 0:
                if USE_LOGGING: print(f'\t\tRight chunk ran out')
                return False

            if l.isnumeric() and r.isnumeric():
                if l == r: break
                else:
                    x = int(l) < int(r)
                    if USE_LOGGING: print(f'\t\tNumeric comparison: Smaller is {l if x else r}')
                    return x

            if l[0] == lBracket and r[0] == lBracket:
                listStack.append(lBracket)
                l = l[1:]
                r = r[1:]
                continue

            if l[0] == lBracket:
                if r[0] == rBracket:
                    if USE_LOGGING: print(f'\t\tLeft was start of list and Right was ending a list')
                    return False
                if r[0] != lBracket:
                    r = f'[{r}]'
                    continue
            elif r[0] == lBracket:
                if l[0] == rBracket:
                    if USE_LOGGING: print(f'\t\Right was start of list and Left was ending a list')
                    return True
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
                    x = l[0] == rBracket
                    b = "Left" if x else "right"
                    if USE_LOGGING: print(f'\t\t{b} list ended first')
                    return x


            if l[-1] == rBracket and r[-1] == rBracket:
                listStack.pop()
                l = l[:-1]
                r = r[:-1]
                continue
            elif l[-1] == rBracket:
                x = int(l[:l.index(rBracket)]) <= int(r)
                if USE_LOGGING:
                    if x:
                        print(f'\t\tLeft List ended first and value was <= right value')
                    else: 
                        print(f'\\tLeft list ended first but value was greater than right value')
                return x
            elif r[-1] == rBracket:
                x = int(l) < int(r[:r.index(rBracket)])
                if USE_LOGGING:
                    if x:
                        print(f'\t\Right List ended first and left value was < right value')
                    else: 
                        print(f'\\Right list ended first value was greater than right value')
                return x

    return True

def getCorrectPackets(input):
    correctIndexes = []
    for i, packetPair in enumerate(input):
        allG = comparePackets2(packetPair[0], packetPair[1])
        
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
    
    USE_DEMO = True
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