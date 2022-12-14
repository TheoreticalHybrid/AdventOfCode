from itertools import chain
import time

USE_LOGGING = False
USE_DEMO = False
PART_ONE = True

def getInput(fileName):
    file = open(fileName, 'r')
    input = file.readlines()

    if USE_LOGGING: print(input)

    return input

headPosition = (0,0)
tailPosition = (0,0)

tailHistory = {0: {0}}
    

def followCommands(commands):
    global headPosition
    global tailPosition

    #move the head
    for c in commands:
        match c.strip().split():
            case 'U', u: 
                headPosition = (headPosition[0], headPosition[1] + int(u)) 
            case 'D', d:
                headPosition = (headPosition[0], headPosition[1] - int(d))
            case 'L', l:
                headPosition = (headPosition[0] - int(l), headPosition[1])
            case 'R', r:
                headPosition = (headPosition[0] + int(r), headPosition[1])

        headX, headY = headPosition[0], headPosition[1]
        tailX, tailY = tailPosition[0], tailPosition[1]
        
        #determine if tail needs to move
        if (abs(headX-tailX) > 1):
            startX = tailX + (1 if headX > tailX else -1)
            endX = startX
            
            for x in range(startX, headX, 1 if headX > tailX else -1):
                if x not in tailHistory:
                    tailHistory[x] = {headY}
                else:
                    tailHistory[x].add(headY)

                endX = x

            tailPosition = (endX, headY)
        elif (abs(headY-tailY) > 1):
            startY = tailY + (1 if headY > tailY else -1)
            yMoves = [*range(startY, headY, 1 if headY > tailY else -1)]
           
            if headX not in tailHistory: tailHistory[headX] = set(yMoves)
            else: tailHistory[headX].update(yMoves)

            tailPosition = (headX, yMoves[-1])

    if USE_LOGGING: print([(k,v) for k in tailHistory.keys() for v in tailHistory[k]])

#start of main
solution = 0

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'

commands = getInput(file)
followCommands(commands)
solution = len([(k,v) for k in tailHistory.keys() for v in tailHistory[k]])

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime) #0.012001752853393555