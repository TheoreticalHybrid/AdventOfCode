import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

def getInput(fileName):
    file = open(fileName, 'r')
    input =  [tuple((int(x) for x in line.split())) for line in file.read().split("\n")]

    if USE_LOGGING: print(input)

    return input

def getListDiff(input):
    list1, list2 = [], []
    for pair in input:
        list1.append(pair[0])
        list2.append(pair[1])

    list1.sort()
    list2.sort()

    sum = 0
    for i, num1 in enumerate(list1):
        sum += abs(num1 - list2[i])

    return sum

def getSimilarityScore(input):
    score = 0

    list1, list2 = [], []
    for pair in input:
        list1.append(pair[0])
        list2.append(pair[1])

    list1.sort()
    list2.sort()

    for num1 in list1:
        matchCount = sum(num2 == num1 for num2 in list2)
        score += (num1 * matchCount)

    return score

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = getListDiff(input)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

startTime = time.time()

solution = getSimilarityScore(input)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)