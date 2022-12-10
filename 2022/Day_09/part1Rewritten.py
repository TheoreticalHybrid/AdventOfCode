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

tailHistory = {tailPosition}
    

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
        #print(f'{tailPosition} -> {headPosition}')
        if (abs(headX-tailX) > 1):
            #move tail
            startX = tailX + (1 if headX > tailX else -1)
            
            for x in range(startX, headX, 1 if headX > tailX else -1):
                tailPosition = (x, headY)
                tailHistory.add(tailPosition)

        elif (abs(headY-tailY) > 1):
            #move tail
            startY = tailY + (1 if headY > tailY else -1)
            moves = [(headX, y) for y in range(startY, headY, 1 if headY > tailY else -1)]
            
            tailHistory.update(moves)

            tailPosition = moves[-1]

    if USE_LOGGING: print(tailHistory)

#start of main
solution = 0

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'

commands = getInput(file)
followCommands(commands)
solution = len(tailHistory)

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime) #0.006005287170410156