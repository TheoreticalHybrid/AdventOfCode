import time
import itertools

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

def getInput(fileName):
    file = open(fileName, 'r')

    input = [line.split() for line in file.readlines()]

    return input

# Built purely for debugging. Augmented solution from Day 10
def testPipeMap():
    file = open('pipeOutput.txt', 'r')
    input = [line for line in file.readlines()]
    total = 0
    
    rowTotals = []
    for row in input: # for each row besides the first and last (impossible to have valid '.' characters there)
        inside = False
        horizontalPipeEnd = None
        for c in row: # for each character in that row
            if c == '-':
                total += 1
            elif c == ' ':
                if inside:
                    total += 1
            elif c == '|': # '|' character always toggles the inside indicator
                inside = not inside
                total += 1
            else:
                if c in ('L', 'F'): # L and F always toggle the inside character
                    inside = not inside
                    horizontalPipeEnd = c # store the character as the beginning of a horizontal pipe segment
                    total += 1
                
                # J and 7 only toggle the inside character if their vertical trajectory is different than that of the start of the horizontal pipe segment
                # For example, F---7 both have the vertical direction pointing downward, but F---J has F pointing downward but J pointing upward
                elif c in ('J', '7'):
                    inside = inside if horizontalPipeEnd == ('F' if c == 'J' else 'L') else not inside
                    total += 1
        rowTotals.append(total)

    print(rowTotals)
    return total    

# Built purely for debugging. Writes the given input as a Day 10 pipe to a file in order to visually confirm correctness
def printPipeMap(input, minX):
    file = open('pipeOutput.txt', 'w')

    for yKey in sorted(input.keys()):
        lastX = minX
        isHorizontalPipe = False
        for xKey in sorted(input[yKey].keys()):
            c = input[yKey][xKey]
            file.write(''.join(['-' if isHorizontalPipe else ' '] * (xKey - lastX)))
            file.write(c)
            lastX = xKey + 1
            isHorizontalPipe = c in ('F', 'L')
            
        file.write('\n')

    file.close()

# Augmented Day 10 solution
def findEnclosedArea(input):
    total = 0

    # rowTotalValidations = [8, 16, 24, 32, 40, 48, 56, 88, 132, 176, 229, 285, 341, 397, 464, 535, 606, 677, 755, 833, 913, 993, 1073, 1153, 1233, 1320, 1407, 1494, 1581, 1668, 1755, 1847, 1939, 2031, 2135, 2257, 2379, 2501, 2623, 2745, 2867, 2989, 3107, 3238, 3358, 3478, 3605, 3732, 3859, 3996, 4133, 4270, 4419, 4566, 4713, 4860, 5007, 5154, 5307, 5460, 5613, 5766, 5907, 6041, 6175, 6309, 6443, 6583, 6722, 6861, 7013, 7165, 7317, 7500, 7683, 7866, 8049, 8247, 8457, 8671, 8885, 9120, 9355, 9602, 9849, 10101, 10349, 10597, 10832, 11067, 11286, 11505, 11733, 11961, 12192, 12412, 12637, 12865, 13081, 13292, 13503, 13714, 13933, 14140, 14356, 14572, 14788, 15011, 15234, 15447, 15669, 15879, 16089, 16287, 16496, 16695, 16894, 17093, 17292, 17485, 17665, 17837, 18009, 18176, 18331, 18490, 18649, 18813, 18977, 19134, 19296, 19459, 19622, 19776, 19951, 20126, 20322, 20519, 20731, 20941, 21165, 21382, 21599, 21823, 22036, 22239, 22442, 22657, 22858, 23059, 23277, 23490, 23716, 23951, 24191, 24431, 24679, 24920, 25155, 25390, 25617, 25841, 26065, 26291, 26514, 26721, 26928, 27146, 27364, 27582, 27800, 28012, 28224, 28436, 28640, 28849, 29066, 29283, 29505, 29727, 29970, 30213, 30464, 30715, 30981, 31247, 31518, 31789, 32051, 32313, 32589, 32865, 33141, 33417, 33677, 33931, 34192, 34460, 34714, 34968, 35222, 35476, 35733, 35994, 36244, 36504, 36764, 37020, 37272, 37520, 37768, 38005, 38248, 38484, 38705, 38926, 39147, 39368, 39594, 39818, 40042, 40266, 40488, 40699, 40919, 41150, 41381, 41612, 41843, 42105, 42377, 42661, 42951, 43241, 43528, 43824, 44120, 44416, 44732, 45061, 45388, 45715, 46044, 46378, 46712, 47057, 47389, 47728, 48070, 48412, 48778, 49144, 49510, 49876, 50245, 50622, 50999, 51385, 51747, 52109, 52487, 52865, 53243, 53620, 53997, 54386, 54775, 55170, 55565, 55960, 56355, 56755, 57144, 57533, 57919, 58305, 58685, 59065, 59453, 59841, 60229, 60626, 61042, 61458, 61874, 62290, 62709, 63128, 63547, 63966, 64385, 64804, 65215, 65626, 66043, 66460, 66885, 67310, 67735, 68160, 68585, 69010, 69435, 69860, 70285, 70713, 71137, 71561, 71985, 72416, 72847, 73286, 73725, 74164, 74603, 75031, 75459, 75883, 76293, 76703, 77109, 77515, 77921, 78327, 78713, 79099, 79485, 79871, 80257, 80629, 81001, 81359, 81717, 82075, 82433, 82791, 83130, 83463, 83786, 84109, 84425, 84741, 85057, 85370, 85663, 85956, 86221, 86499, 86773, 87038, 87303, 87544, 87785, 88026, 88254, 88482, 88698, 88898, 89082, 89266, 89450, 89611, 89756, 89901, 90042, 90176, 90290, 90397, 90504, 90590, 90676, 90762, 90867, 90961, 91067, 91173, 91279, 91358, 91422, 91486, 91546, 91584, 91622, 91660, 91698, 91727, 91753, 91786, 91819, 91846, 91873, 91900, 91927, 91954, 91981, 92008, 92035, 92056, 92077, 92108, 92139, 92170, 92201, 92232, 92270, 92308, 92346, 92384, 92422, 92453, 92475, 92497, 92519, 92541, 92563, 92585, 92607, 92626, 92645, 92664, 92683, 92688, 92693, 92698, 92703, 92714, 92725, 92736, 92747, 92758]

    for i, yKey in enumerate(sorted(input.keys())): # for every y index (sorted)
        inside, hZone = False, False # I'll be honest, I had to fiddle with the hZone thing a lot to get it to work and I still don't fully understand it
        horizontalPipeEnd, insideX = None, None
        for xKey in sorted(input[yKey].keys()): # for every x index (sorted) for this y
            c = input[yKey][xKey]
            if c == '|': # '|' character always toggles the inside indicator
                if inside:
                    inside = hZone = False
                    total += (xKey + 1 - insideX) # Add to total the (inclusive) difference between this x index and the x index of the start of the pipe/hole
                else:
                    inside = True
                    insideX = xKey
            else:
                if c in ('L', 'F'):
                    if inside:
                        hZone = True
                    else:
                        inside = True
                        insideX = xKey
                    horizontalPipeEnd = c # store the character as the beginning of a horizontal pipe segment
                elif c in ('J', '7'):
                    if horizontalPipeEnd == ('F' if c == 'J' else 'L'):
                        if hZone:
                            inside = hZone = False
                            total += (xKey + 1 - insideX)
                    else:
                        if hZone:
                            hZone = False
                        else:
                            inside = hZone = False
                            total += (xKey + 1 - insideX)

        #if total != rowTotalValidations[i]:
            #raise ValueError(f'Row {i} is wrong!')

    return total

def getLagoonSize(input):
    #Build input parameters that are only Direction and Length
    digInstructions = []
    for direction, length, color in input:
        if PART_ONE:
            digInstructions.append((direction, int(length)))
        else:
            ds = ['R','D','L','U']
            l = color[2:7]
            newLength = int('0x'+l, 0)
            digInstructions.append((ds[int(color[7:8])], newLength))

    firstMove, lastMove = None, None

    xCoord, yCoord, minX = 0, 0, 0
    digLocations = {yCoord: {xCoord: 'S'}} # key = yValue, value = dictionary(key = xValue, value = pipe character)
    for direction, length in digInstructions:
        if firstMove == None: firstMove = direction

        if lastMove is not None:
            match lastMove:
                case 'R': digLocations[yCoord][xCoord] = 'J' if direction == 'U' else '7'
                case 'L': digLocations[yCoord][xCoord] = 'L' if direction == 'U' else 'F'
                case 'U': digLocations[yCoord][xCoord] = '7' if direction == 'L' else 'F'
                case 'D': digLocations[yCoord][xCoord] = 'J' if direction == 'L' else 'L'

        coords = []
        match direction:
             case 'R':
                newX = xCoord + length
                coords = [(newX, yCoord)]
                xCoord = newX
             case 'L':
                newX = xCoord - length
                coords = [(newX, yCoord)]
                xCoord = newX
             case 'D':
                newY = yCoord + length
                coords = list(zip(itertools.repeat(xCoord), range(yCoord + 1, newY + 1)))
                yCoord = newY
             case 'U':
                newY = yCoord - length
                coords = list(zip(itertools.repeat(xCoord), range(newY, yCoord)))
                yCoord = newY
        minX = min(minX, xCoord)

        for c in coords:
            x, y = c
            if y not in digLocations: digLocations[y] = {}
            if x not in digLocations[y]:
                if direction in ('U','D'):
                    digLocations[y][x] = '|'
                # digLocations[y][x] = '-' if direction in ('R','L') else '|' # I don't actually need to do the horizontal pipes
            elif c == (0, 0):
                match firstMove:
                    case 'R': digLocations[0][0] = 'F' if direction == 'U' else 'L'
                    case 'L': digLocations[0][0] = '7' if direction == 'U' else 'J'
                    case 'U': digLocations[0][0] = 'L' if direction == 'L' else 'J'
                    case 'D': digLocations[0][0] = '7' if direction == 'L' else 'F'
            else:
                print(f'Duplicate dig site: ({yCoord},{xCoord})') #raise ValueError(f'Duplicate dig site: ({xCoord},{yCoord})')
                pass
        
        lastMove = direction


    #if USE_LOGGING: 
        #printPipeMap(digLocations, minX)
        #testPipeMap()

    return findEnclosedArea(digLocations)

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

solution = getLagoonSize(input)

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)