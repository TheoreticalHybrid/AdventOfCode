from itertools import chain
import time

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

def getInput(fileName):
    file = open(fileName, 'r')
    input = file.readlines()

    if USE_LOGGING: print(input)

    return input

knotPositions = [(0,0)] * 10
tailHistory = {(0,0)}

def adjustTail():
    for k in range(1,10):
        localHead = knotPositions[k-1]
        localTail = knotPositions[k]

        xDiff = localHead[0] - localTail[0]
        yDiff = localHead[1] - localTail[1]

        if abs(xDiff) < 2 and abs(yDiff) < 2: break #Knots are adjacent, no more moves to be done

        newX = localTail[0] + (1 if xDiff > 0 else -1 if xDiff < 0 else 0)
        newY = localTail[1] + (1 if yDiff > 0 else -1 if yDiff < 0 else 0)
        newPosition = (newX, newY)

        if USE_LOGGING: print(f'\tKnot {k} moved to {newPosition}')

        knotPositions[k] = newPosition
        if k == 9: tailHistory.add(newPosition)

def followCommands(commands):
    
    for c in commands:
        if USE_LOGGING: print(c)

        head = knotPositions[0]
        headMoves = []

        match c.strip().split():
            case 'U', u: 
                headMoves = [(head[0], head[1] + y) for y in range(1, int(u) + 1)]
            case 'D', d:
                headMoves = [(head[0], head[1] - y) for y in range(1, int(d) + 1)]
            case 'L', l:
                headMoves = [(head[0] - x, head[1]) for x in range(1, int(l) + 1)]
            case 'R', r:
                headMoves = [(head[0] + x, head[1]) for x in range(1, int(r) + 1)]
        
        for move in headMoves:
            knotPositions[0] = move
            adjustTail()


#start of main
solution = 0

startTime = time.time()

file = 'example2.txt' if USE_DEMO else 'input1.txt'

if USE_LOGGING: print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

commands = getInput(file)
followCommands(commands)

if USE_LOGGING: 
    for point in sorted(tailHistory): 
        print(point)

solution = len(tailHistory)

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime) #0.03854012489318848