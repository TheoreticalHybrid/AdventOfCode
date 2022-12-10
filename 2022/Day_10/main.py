import time
import os
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

CRT_WIDTH = 40

xRegister = [1]

def getInput(fileName):
    file = open(fileName, 'r')
    input = file.readlines()

    if USE_LOGGING: input

    return input

def executeInstruction(instruction):
    command = instruction[0]
    xValue = xRegister[-1]

    match command:
        case "noop": xRegister.append(xValue)
        case "addx":
            xRegister.append(xValue)
            xRegister.append(xValue + int(instruction[1]))

#start of main
solution = 0

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'

input = getInput(file)

for command in input:
    executeInstruction(command.split())

if (PART_ONE):
    for c in [20, 60, 100, 140, 180, 220]:
        xValue = xRegister[c-1]
        print(f'Clock {c} = {xValue}')
        solution += (xValue * c)
else:
    for i in range(len(xRegister)):
        crtVal = i%CRT_WIDTH
        if i > 0 and crtVal == 0: print()

        print("#" if abs(xRegister[i] - crtVal) < 2 else ".", end = " ")

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime)