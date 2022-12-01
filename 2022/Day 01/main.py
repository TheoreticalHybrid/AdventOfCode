import time
import os

def getCalorieList(fileName, log = False):
    file = open(fileName, 'r')
    #input =  [int(x) for x in file.read().split("\n\n")]
    input =  [sum((int(y) for y in x.split("\n"))) for x in file.read().split("\n\n")]

    if log: print(input)

    return input

def getMaxCaloriesSum(input, numMaxes):
    maxSum = 0

    for i in range(0, numMaxes):
        thisMax = max(input)
        maxSum += thisMax
        input.remove(thisMax)

    return maxSum


useDemo = False
useLogging = False

startTime = time.time()

file = 'example.txt' if useDemo else 'input1.txt'
calories = getCalorieList(file, useLogging)
solution = getMaxCaloriesSum(calories, 3)

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)