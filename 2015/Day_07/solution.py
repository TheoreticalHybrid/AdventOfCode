import sys
import time
from pathlib import Path

options = [opt for opt in sys.argv[1:] if opt.startswith("-")]
arguments = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

USE_LOGGING = '-v' in options
USE_DEMO = '-d' in options

if '-f' in options:
    #Ask for user input to keep going
    userInput = input("File: ")
    my_file = Path(userInput)
    if not my_file.is_file():
        raise SystemExit(f"File {userInput} is not found")

def getProblemInput(fileName):
    problemData = ''
    with open(fileName, 'r') as file:
        problemData = [l.strip() for l in file.readlines()]

    return problemData

def performBitwiseAnd(value1, value2):
    return value1 & value2

def performBitwiseOr(value1, value2):
    return value1 | value2

def performLeftShift(value, shiftAmount):
    return value << shiftAmount

def performRightShift(value, shiftAmount):
    return value >> shiftAmount

def performBitwiseNot(value):
    return ~value & 0xFFFF

def buildCircuit(instructions, goalWire):
    wireSignals = dict()

    instQueue = list(instructions)

    while any(instQueue):
        instruction = instQueue.pop(0)
        operation, outputWire = instruction.split(' -> ')
        operationElements = operation.split(' ')

        if len(operationElements) == 1:
            if operation.isdigit(): wireSignals[outputWire] = int(operation) # wire signal assignment
            elif operation in wireSignals: wireSignals[outputWire] = wireSignals[operation]
            else: instQueue.append(instruction)
        elif operationElements[0] == 'NOT':
            w = operationElements[1]
            if w in wireSignals: wireSignals[outputWire] = performBitwiseNot(wireSignals[w])
            else: instQueue.append(instruction)
        else:
            arg1, op, arg2 = operationElements
            var1, var2 = None, None
            func = None
            match op:
                case 'AND':
                    func = performBitwiseAnd
                    if arg1.isdigit(): var1 = int(arg1)
                    elif arg1 in wireSignals: var1 = wireSignals[arg1]
                    
                    if arg2.isdigit(): var2 = int(arg2)
                    elif arg2 in wireSignals: var2 = wireSignals[arg2]
                case 'OR':
                    func = performBitwiseOr
                    if arg1.isdigit(): var1 = int(arg1)
                    elif arg1 in wireSignals: var1 = wireSignals[arg1]
                    
                    if arg2.isdigit(): var2 = int(arg2)
                    elif arg2 in wireSignals: var2 = wireSignals[arg2]
                case 'LSHIFT':
                    func = performLeftShift
                    if arg1.isdigit(): var1 = int(arg1)
                    elif arg1 in wireSignals: var1 = wireSignals[arg1]
                    
                    if arg2.isdigit(): var2 = int(arg2)
                    elif arg2 in wireSignals: var2 = wireSignals[arg2]
                case 'RSHIFT':
                    func = performRightShift
                    if arg1.isdigit(): var1 = int(arg1)
                    elif arg1 in wireSignals: var1 = wireSignals[arg1]
                    
                    if arg2.isdigit(): var2 = int(arg2)
                    elif arg2 in wireSignals: var2 = wireSignals[arg2]

            if var1 is None or var2 is None: instQueue.append(instruction)
            else: wireSignals[outputWire] = func(var1, var2)

    return wireSignals[goalWire]

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = buildCircuit(problemInput, 'a')

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    #exit()
    print('---------PART TWO---------')
    startTime = time.time()

    index = [i for i in range(len(problemInput)) if problemInput[i].endswith('-> b')][0]
    problemInput[index] = f'{solution} -> b'
    solution = buildCircuit(problemInput, 'a')

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)