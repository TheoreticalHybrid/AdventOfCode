import time

USE_LOGGING = True
USE_DEMO = True
PART_ONE = False

characterMap = {'|': (0,1), '-': (1,0), 'L': (1,-1), 'J': (-1,-1), '7': (-1,1), 'F': (1,1)}
startingPoint = (0,0)

def getInput(fileName):
    global startingPoint
    file = open(fileName, 'r')

    input = []
    
    for i,line in enumerate(file.readlines()):
        lineMap = []
        for j,c in enumerate(line.strip()):
            if c == 'S': startingPoint = (i,j)

            lineMap.append(c)
        input.append(lineMap)

    if USE_LOGGING:
        for line in input: print(line)

    return input

def moveLeft(c):
    match c:
        case '-':
            return 'l'
        case 'L':
            return 'u'
        case 'F':
            return 'd'

def moveRight(c):
    match c:
        case '-':
            return 'r'
        case '7':
            return 'd'
        case 'J':
            return 'u'

def moveUp(c):
    match c:
        case '|':
            return 'u'
        case '7':
            return 'l'
        case 'F':
            return 'r'

def moveDown(c):
    match c:
        case '|':
            return 'd'
        case 'L':
            return 'r'
        case 'J':
            return 'l'
        
def findFirstMove():
    myIndex = startingPoint
    ix, iy = myIndex[0], myIndex[1]
    if iy > 0 and input[ix][iy-1] in ('-', 'L', 'F'): # connects to left cell
        return 'l'
    elif iy < len(input[0]) and input[ix][iy+1] in ('-', 'J', '7'): # connects to right cell
        return 'r'
    elif ix > 0 and input[ix-1][iy] in ('|', '7', 'F'): # connects to above cell
        return 'u'
    elif ix < len(input) and input[ix+1][iy] in ('|', 'L', 'J'): # connects to below cell
        return 'd'

def buildLoop(input):
    loop = [('S', startingPoint)]
    d = findFirstMove()

    shifts = {'u': (-1, 0), 'd': (1, 0), 'r': (0, 1), 'l': (0, -1)}

    myIndex = startingPoint
    returnedToStart = False
    while not returnedToStart:
        s = shifts[d]
        sx, sy = myIndex[0] + s[0], myIndex[1] + s[1]
        sc = input[sx][sy]
        loop.append((sc, (sx,sy)))
        myIndex = (sx,sy)

        if sc == 'S':
            returnedToStart = True
        else:
            match d:
                case 'u':
                    d = moveUp(sc)
                case 'd':
                    d = moveDown(sc)
                case 'r':
                    d = moveRight(sc)
                case 'l':
                    d = moveLeft(sc)

    return loop

# I don't know if there are irrelevant pipes within the loop, and I need to
# remove the distractions for analysis
def replaceGarbagePipes(input, loop):
    newInput = []

    for i,row in enumerate(input):
        newRow = []
        for j,c in enumerate(row):
            newC = 'X'
            if c in ('.', 'S'): newC = c
            else:
                for pipe in filter(lambda p: p[0] == c, loop):
                    if pipe[1][0] == i and pipe[1][1] == j:
                        newC = c
            newRow.append(newC)

        newInput.append(newRow)

    return newInput

def findEnclosedArea(loop):
    pass

startTime = time.time()

file = ('example1.txt' if PART_ONE else 'example2.txt') if USE_DEMO else 'input1.txt'
input = getInput(file)
loop = buildLoop(input)

solution = 0
if PART_ONE: solution = len(loop) // 2
else:
    input = replaceGarbagePipes(input, loop)
    if USE_LOGGING: 
        for row in input: print(''.join(row))

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)