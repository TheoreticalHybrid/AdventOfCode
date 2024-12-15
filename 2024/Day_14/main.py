import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

def getInput(fileName):
    input = []

    with open(fileName, 'r') as file:
       for line in file.readlines():
           position, velocity = line.strip().split(' ')
           py, px = position[2:].split(',')
           vy, vx = velocity[2:].split(',')
           input.append(((int(px), int(py)), (int(vx), int(vy))))

    if USE_LOGGING:
        for m in input:
            print(m)

    return input

def getSafetyFactor(size, robots):
    endRobotPositions = []
    waitTime = 100

    for r in robots:
        robotPosition, robotVelocity = r
        endX, endY = (robotPosition[0] + (robotVelocity[0] * waitTime)) % size[0], (robotPosition[1] + (robotVelocity[1] * waitTime)) % size[1]
        endRobotPositions.append((endX, endY))

    quadrants = [0] * 4
    middleX, middleY = size[0] // 2, size[1] // 2

    for erp in endRobotPositions:
        erpX, erpY = erp
        if erpX < middleX:
            if erpY < middleY: quadrants[0] = quadrants[0] + 1
            elif erpY > middleY: quadrants[1] = quadrants[1] + 1
        elif erpX > middleX:
            if erpY < middleY: quadrants[2] = quadrants[2] + 1
            elif erpY > middleY: quadrants[3] = quadrants[3] + 1

    solution = 1
    for q in quadrants: solution = solution * q
    
    return solution

def fuckItIGuessIWillSaveEachOneAndLookManually(size, robots):
    keepSearching = True
    imageNumber = 0
    pageSize = 1000

    solution = 0

    while keepSearching:
        for i in range(imageNumber, pageSize):
            nextPositions = []
            for r in robots:
                rp, rv = r
                nextP = tuple(map(lambda x, y, s: (x + y) % s, rp, rv, size))
                nextPositions.append((nextP, rv))

            #save image to file
            fileName = f'snapshot_{str(i).rjust(5, "0")}.txt'
            with open(fileName, "w") as f:
                lines = [[' ' for y in range(size[1])] for x in range(size[0])]
                for np in nextPositions:
                    npX, npY = np[0]
                    lines[npX][npY] = '#'

                f.writelines([f'{''.join(l)}\n' for l in lines])

            robots = nextPositions
        imageNumber += pageSize
        pageSize += pageSize

        #Ask for user input to keep going
        userInput = input("Enter valid number for solution to quit:")
        if userInput.isdigit():
            keepSearching = False
            solution = int(userInput)

    return solution

exampleFile = 'example.txt'
file = exampleFile if USE_DEMO else 'input1.txt'
problemInput = getInput(file)
#exit()

size = (7,11) if USE_DEMO else (103,101)

startTime = time.time()

solution = getSafetyFactor(size, problemInput)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print('Part 1 Completion time: ', endtime - startTime)

#exit()
print('---------PART TWO---------')
startTime = time.time()

solution = fuckItIGuessIWillSaveEachOneAndLookManually(size, problemInput)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)