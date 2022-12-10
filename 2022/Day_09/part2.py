from itertools import chain
import time

USE_LOGGING = True
SUPER_LOGGING = False
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
    
    for c in commands:
        if USE_LOGGING: print(c)

        match c.strip().split():
            case 'U', u: 
                headPosition = (headPosition[0], headPosition[1] + int(u))
            case 'D', d:
                headPosition = (headPosition[0], headPosition[1] - int(d))
            case 'L', l:
                headPosition = (headPosition[0] - int(l), headPosition[1])
            case 'R', r:
                headPosition = (headPosition[0] + int(r), headPosition[1])

        localHeadPosition = headPosition
        
        for knot in range(9): #I can't be bothered to make this data driven today
            localTailPosition = tailHistories[knot][-1]
            positionDiff = tuple(map(lambda i, j: i - j, localHeadPosition, localTailPosition))
            diffX, diffY = positionDiff[0], positionDiff[1]
            #headX, headY = localHeadPosition[0], localHeadPosition[1]
            tailX, tailY = localTailPosition[0], localTailPosition[1]

            if SUPER_LOGGING: print(f'\t\tKnot {knot + 1}: {localHeadPosition} - {localTailPosition} = {positionDiff}')

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
                
                diff = len(xRange) - len(yRange)
                
                if diff < 0:
                    xRange += [xRange[-1]] * abs(diff)
                elif diff > 0:
                    yRange += [yRange[-1]] * diff

            for i,j in zip(xRange, yRange):                
                if abs(localHeadPosition[0] - localTailPosition[0]) < 2 and abs(localHeadPosition[1] - localTailPosition[1]) < 2:
                    break

                localTailPosition = (tailX + i, tailY + j)
                if SUPER_LOGGING: print(f'\t\t{(tailX, tailY)} + {(i,j)} = {localTailPosition}')
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
seen = set()
unique9set = [x for x in tailHistories[-1] if x not in seen and not seen.add(x)]
if USE_LOGGING: 
    for point in unique9set: 
        print(point)
solution = len(unique9set)

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime) #0.006005287170410156