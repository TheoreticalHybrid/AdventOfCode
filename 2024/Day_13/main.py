import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

def getInput(fileName):
    input = []

    with open(fileName, 'r') as file:
        for machine in file.read().split('\n\n'):
            detes = machine.split('\n')
            buttonA = tuple(int(n.strip().split('+')[1]) for n in detes[0].split(':')[1].split(','))
            buttonB = tuple(int(n.strip().split('+')[1]) for n in detes[1].split(':')[1].split(','))
            prize = tuple(int(n.strip().split('=')[1]) for n in detes[2].split(':')[1].split(','))
            input.append((buttonA, buttonB, prize))

    if USE_LOGGING:
        for m in input:
            print(m)

    return input

def getBestMachineCostBetter(buttonA, buttonB, prize, partTwo):
    bestCost = 0
    aCost = 3
    bCost = 1
    ax, ay = buttonA
    bx, by = buttonB
    px, py = prize

    if partTwo:
        px += 10000000000000
        py += 10000000000000



    return bestCost

def getBestMachineCost(buttonA, buttonB, prize):
    bestCost = 0
    aCost = 3
    bCost = 1
    ax, ay = buttonA
    bx, by = buttonB
    px, py = prize

    axMax, ayMax = px // ax, py // ay
    bxMax, byMax = px // bx, py // by
    aMax = min(axMax, ayMax, 100)
    bMax = min(bxMax, byMax, 100)

    for i in range(1, max(aMax, bMax) + 1):
        if i < aMax:
            tax, tay = i * ax, i * ay
            if tax <= px and tay <= py:
                bxDiff, byDiff = px - tax, py - tay
                bxMod, byMod = bxDiff % bx, byDiff % by
                bxDiv, byDiv = bxDiff // bx, byDiff // by
                if bxMod == 0 and byMod == 0 and bxDiv == byDiv:
                    # found a potential solution
                    cost = (i * aCost) + (bxDiv * bCost)
                    bestCost = cost if bestCost == 0 else min(bestCost, cost)
                    if USE_LOGGING: print(f'Found potential solution: A-{i} B-{bxDiv}')

        if i < bMax:
            tbx, tby = i * bx, i * by
            if tbx <= px and tby <= py:
                axDiff, ayDiff = px - tbx, py - tby
                axMod, ayMod = axDiff % ax, ayDiff % ay
                axDiv, ayDiv = axDiff // ax, ayDiff // ay
                if axMod == 0 and ayMod == 0 and axDiv == ayDiv:
                    # found a potential solution
                    cost = (i * bCost) + (axDiv * aCost)
                    bestCost = cost if bestCost == 0 else min(bestCost, cost)
                    if USE_LOGGING: print(f'Found potential solution: A-{axDiv} B-{i}')


    return bestCost

exampleFile = 'example.txt'
file = exampleFile if USE_DEMO else 'input1.txt'
input = getInput(file)
#exit()

startTime = time.time()

solution = 0

machineNumber = 1
for machine in input:
    if USE_LOGGING: print(f'Testing Machine {machineNumber}')
    bestCost = getBestMachineCost(machine[0], machine[1], machine[2])
    if USE_LOGGING: print(f'Machine {machineNumber} best cost: {bestCost}')
    solution += bestCost
    machineNumber += 1

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
print('---------PART TWO---------')
startTime = time.time()

solution = 0

machineNumber = 1
for machine in input:
    if USE_LOGGING: print(f'Testing Machine {machineNumber}')
    bestCost = getBestMachineCostBetter(machine[0], machine[1], machine[2], True)
    if USE_LOGGING: print(f'Machine {machineNumber} best cost: {bestCost}')
    solution += bestCost
    machineNumber += 1

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)