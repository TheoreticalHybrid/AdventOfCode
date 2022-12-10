from itertools import chain
import time

USE_LOGGING = True
USE_DEMO = True
PART_ONE = False

def getInput(fileName):
    file = open(fileName, 'r')
    input = file.readlines()

    if USE_LOGGING: print(input)

    return input

headPosition = (0,0)

tailHistories = [[(0,0)] for x in range(9)]

def followCommands(commands):
    global headPosition
    
    for c in commands[:2]:
        if USE_LOGGING: print(c)
        xMove = False

        match c.strip().split():
            case 'U', u: 
                headPosition = (headPosition[0], headPosition[1] + int(u))
            case 'D', d:
                headPosition = (headPosition[0], headPosition[1] - int(d))
            case 'L', l:
                headPosition = (headPosition[0] - int(l), headPosition[1])
                xMove = True
            case 'R', r:
                headPosition = (headPosition[0] + int(r), headPosition[1])
                xMove = True

        localHeadPosition = headPosition
        
        for knot in range(9): #I can't be bothered to make this data driven today
            localTailPosition = tailHistories[knot][-1]
            positionDiff = tuple(map(lambda i, j: i - j, localHeadPosition, localTailPosition))
            diffX, diffY = positionDiff[0], positionDiff[1]
            #headX, headY = localHeadPosition[0], localHeadPosition[1]
            tailX, tailY = localTailPosition[0], localTailPosition[1]

            if USE_LOGGING: print(f'\t\tKnot {knot + 1}: {localHeadPosition} - {localTailPosition} = {positionDiff}')

            xmod = 1 if diffX > 0 else -1 if diffX < 0 else 0
            ymod = 1 if diffY > 0 else -1 if diffY < 0 else 0

            if xmod == ymod == 0: 
                if USE_LOGGING: print(f'\t\tBreak on knot {knot + 1}')
                break
            
            xRange = []
            yRange = []

            if diffX == 0:
                yRange = list(range(1 * ymod, diffY, ymod))
                xRange = [0] * len(yRange)
            elif diffY == 0:
                xRange = list(range(1 * xmod, diffX, xmod))
                yRange = [0] * len(xRange)
            else:
                xRange = list(range(1 * xmod, diffX + xmod, xmod))
                yRange = list(range(1 * ymod, diffY + ymod, ymod))

                if xMove: xRange = xRange[:-1]
                else: yRange = yRange[:-1]
                
                diff = len(xRange) - len(yRange)
                
                if diff < 0:
                    #print(xRange)
                    xRange += [xRange[-1]] * abs(diff)
                elif diff > 0:
                    #print(yRange)
                    yRange += [yRange[-1]] * diff

            for i,j in zip(xRange, yRange):
                localTailPosition = (tailX + i, tailY + j)
                if USE_LOGGING: print(f'\t\t{(tailX, tailY)} + {(i,j)} = {localTailPosition}')
                tailHistories[knot].append(localTailPosition)

            if USE_LOGGING: print(f'\tKnot {knot + 1} ended at {localTailPosition}')
            localHeadPosition = localTailPosition

            if USE_LOGGING: print()

    #if USE_LOGGING: print(tailHistories)


#start of main
solution = 0

startTime = time.time()

file = 'example2.txt' if USE_DEMO else 'input1.txt'

if USE_LOGGING: print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

commands = getInput(file)
followCommands(commands)
solution = len(list(set(tailHistories[-1])))

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime) #0.006005287170410156