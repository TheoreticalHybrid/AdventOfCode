from enum import Enum
from functools import cmp_to_key
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
            bracketStack = []
            for i,c in enumerate(packet):
                if c == lBracket: bracketStack.append(c)
                elif c == rBracket: bracketStack.pop()

                if not bracketStack:
                    listItem = packet[:i+1]
                    internalList = convertPacket(listItem)
                    packetList.append(internalList)
                    packet = packet[i+1:].strip()
                    break
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

def compareLists(leftList, rightList):

    lLen,rLen = len(leftList),len(rightList)
    listDiff = lLen - rLen # positive: left is longer, 0: equal length, negative: right is longer

    for i in range(min(lLen, rLen)):
        l, r = leftList[i],rightList[i]
        lType,rType = type(l),type(r)
        
        if lType is int and rType is int:
            if l == r: continue
            else: return l < r

        if lType is int: l = [l]
        elif rType is int: r = [r]

        result = compareLists(l,r)
        if result is None: continue
        else: return result

    #if we reached here, we ran out of items
    return None if listDiff == 0 else listDiff < 0


def comparePackets(leftPacket, rightPacket):
    leftIsSmaller = compareLists(leftPacket, rightPacket)

    #it'd be better to rewrite compareLists to return these numbers but this is faster
    return 0 if leftIsSmaller is None else -1 if leftIsSmaller else 1

def getCorrectPackets(input):
    correctIndexes = []
    for i, packetPair in enumerate(input):
        allG = comparePackets(convertPacket(packetPair[0]), convertPacket(packetPair[1])) < 0
        
        if USE_LOGGING:
            keyword = 'CORRECT' if allG else 'WRONG'
            print(f'PACKETS ARE IN THE {keyword} ORDER')

        if allG: correctIndexes.append(i)

    return correctIndexes

def findDecoderKey(input):
    # first convert all packets
    packets = []
    for packetPair in input:
        packets.append(convertPacket(packetPair[0]))
        packets.append(convertPacket(packetPair[1]))
    
    # then add divider packets
    divider1 = [[2]]
    divider2 = [[6]]
    packets.append(divider1)
    packets.append(divider2)

    # then organize packets
    packets.sort(key=cmp_to_key(comparePackets))

    # find index of divider packets
    div1Index = packets.index(divider1) + 1
    div2Index = packets.index(divider2) + 1

    # multiply indeces together
    return div1Index * div2Index

def main(argv):
    global USE_DEMO
    global USE_LOGGING
    global PART_ONE
    
    solution = 0

    opts, args = getopt.getopt(argv, "elt")
    for opt, arg in opts:
        match opt:
            case "-e":
                USE_DEMO = True
            case "-l":
                USE_LOGGING = True
            case "-t":
                PART_ONE = False
    
    #USE_DEMO = True
    #USE_LOGGING = True
    #PART_ONE = False

    startTime = time.perf_counter()

    file = 'example.txt' if USE_DEMO else 'input1.txt'

    input = getInput(file)

    if PART_ONE:
        correctPackets = getCorrectPackets(input)
        if USE_LOGGING: print(correctPackets)
        solution = sum(correctPackets) + len(correctPackets)
    else:
        solution = findDecoderKey(input)


    endtime = time.perf_counter()

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])