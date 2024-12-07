import time
import os
import re
import itertools

USE_LOGGING = False
USE_DEMO = False

def getInput(fileName):
    global Rules
    file = open(fileName, 'r')
    input = [(int(line.split(':')[0]), [int(x) for x in line.split(':')[1].strip().split()]) for line in file.readlines()]

    if USE_LOGGING: print(input)

    return input

def getBase3(base10Number):
    digits = []
    while base10Number:
        digits.append(str(base10Number % 3))
        base10Number = base10Number // 3
    digits.reverse()
    return ''.join(digits)

def getCalibrationResult(input, operators):
    sum = 0

    for equation in input:
        goal = equation[0]
        
        numOperationsNeeded = len(equation[1])-1
        for n in range(pow(len(operators), numOperationsNeeded)):
            baseNumber = (bin(n)[2:] if len(operators) == 2 else getBase3(n)).rjust(numOperationsNeeded, '0')
            operatorIndexes = [int(c) for c in baseNumber]
            equationOutput = equation[1][0]
            
            for oi, op in enumerate(operatorIndexes):
                match operators[op]:
                    case '*':
                        equationOutput = equationOutput * equation[1][oi+1]
                    case '+':
                        equationOutput = equationOutput + equation[1][oi+1]
                    case '||':
                        equationOutput = int(str(equationOutput) + str(equation[1][oi+1]))
            
            if equationOutput == goal:
                sum += goal
                break

    return sum

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = getCalibrationResult(input, ['*', '+'])

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()
if USE_LOGGING: print('---------PART TWO---------')
startTime = time.time()

solution = getCalibrationResult(input, ['*', '+', '||']) #Slow, but straightforward. Not sure of a more efficient way to do it

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)