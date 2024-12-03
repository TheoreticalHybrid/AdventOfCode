import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

def getInput(fileName):
    file = open(fileName, 'r')
    input =  [line for line in file.readlines()]

    if USE_LOGGING: print(input)

    return input

def performOperation(command):
    if command.startswith("mul("):
        num1 = int(command[4:].split(',')[0])
        num2 = int(command[4:].split(',')[1][:-1])

        if USE_LOGGING: print(f'COMMAND: {num1} * {num2}')
        return num1 * num2

def getSolution(input, part2):
    sum = 0

    operationsEnabled = True

    for line in input:
        regex = "mul\([0-9][0-9]?[0-9]?,[0-9][0-9]?[0-9]?\)|do\(\)|don't\(\)" if part2 else "mul\([0-9][0-9]?[0-9]?,[0-9][0-9]?[0-9]?\)"
        results = re.findall(regex, line)
        for command in results:
            if command == "do()": operationsEnabled = True
            elif command == "don't()": operationsEnabled = False
            elif operationsEnabled: sum += performOperation(command)

    return sum

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = getSolution(input, False)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()

if USE_DEMO: input = getInput('example2.txt')

startTime = time.time()

solution = getSolution(input, True)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)