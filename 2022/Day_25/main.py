from enum import Enum
import getopt
from itertools import chain, permutations
import math
import sys
import time
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = True

def getCharacterValue(c):
    return -2 if c == '=' else -1 if c == '-' else int(c)

def FromBase5(value):
    numericValue = 0
    for i,c in enumerate(reversed(value)):
        numericValue += math.pow(5, i) * getCharacterValue(c)

    return int(numericValue)

def getInput(fileName):
    global MoveDictionary

    file = open(fileName, 'r')
    
    #input = [FromBase5(row.strip()) for row in file.readlines()]
    input = [row.strip()[::-1] for row in file.readlines()]

    maxLength = len(max(input, key=len))
    input = [v.ljust(maxLength, '0') for v in input]

    if USE_LOGGING: print(input)

    return input

def ToBase5(value):
    newString = []

    index = 0
    while value >=5:
        remainder = int(value)%5
        value = int(math.floor(value/5))

        if len(newString) == index: newString.append('0')
        indexString = newString[index]
        indexValue = getCharacterValue(indexString)

        if remainder < 3:
            pass
        else:
            if len(newString) <= index + 1: newString.append('0')
            pass
            

        index += 1

def getSNAFUsum(values):
    sumList = [0] * (len(values[0])+2)
    
    for i in range(len(values[0])):
        columnSum = 0
        for v in values:
            c = v[i]
            match c:
                case '=':
                    columnSum += -2
                case '-':
                    columnSum += -1
                case _:
                    columnSum += int(c)

        

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
    
    USE_DEMO = True
    USE_LOGGING = True
    #PART_ONE = False

    startTime = time.perf_counter()

    file = 'example.txt' if USE_DEMO else 'input1.txt'

    input = getInput(file)

    if PART_ONE:
        #sumTotal = sum(input)
        pass

    endtime = time.perf_counter()

    print('Solution: ', solution)
    print ('Completion time: ', endtime - startTime)

if __name__ == "__main__":
    main(sys.argv[1:])