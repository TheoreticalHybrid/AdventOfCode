import time
from copy import deepcopy
import itertools

USE_LOGGING = True
USE_DEMO = False
PART_ONE = True

def getInput(fileName):
    file = open(fileName, 'r')

    input = []
    for r in file.readlines():
        coords = tuple(tuple(int(x) for x in c.split(',')) for c in r.strip().split('~'))
        input.append(coords if coords[0][-1] <= coords[1][-1] else (coords[1],coords[0]))

    return input

def getSafeBlocks(input):
    # sort by z values
    input.sort(key=lambda z: z[0][-1])
    shiftedStack = []

    # shift the blocks as far downward as possible
    for block in input:
        c1, c2 = block
        x1,y1,z1 = c1
        x2,y2,z2 = c2

        lowerBlockZ = 0
        for b in shiftedStack:
            b1, b2 = b
            bx1, by1, bz1 = b1
            bx2, by2, bz2 = b2

            xInt = range(max(x1, bx1), min(x2, bx2)+1)
            yInt = range(max(y1, by1), min(y2, by2)+1)

            if len(xInt) > 0 and len(yInt) > 0:
                lowerBlockZ = bz2 # should already be sorted so bz2 should be the higher
        c1 = (x1,y1,lowerBlockZ + 1)
        c2 = (x2,y2,lowerBlockZ + 1 + (z2 - z1))
        shiftedStack.append((c1, c2))

    if False and USE_LOGGING:
        for block in shiftedStack:
            print(f'{block[0]} - {block[1]}')

    touchingBlocks = {} # key=block, value=([list of above touchers],[list of below touchers])
    for i, block in enumerate(shiftedStack):
        # get block coords
        a1,a2 = block
        ax1, ay1, az1 = a1
        ax2, ay2, az2 = a2

        if block not in touchingBlocks: touchingBlocks[block] = ([],[])

        for nextBlock in shiftedStack[i+1:]:
            b1,b2 = nextBlock
            bx1, by1, bz1 = b1
            bx2, by2, bz2 = b2

            xInt = range(max(ax1, bx1), min(ax2, bx2)+1)
            yInt = range(max(ay1, by1), min(ay2, by2)+1)

            if az2 + 1 == bz1 and len(xInt) > 0 and len(yInt) > 0:
                touchingBlocks[block][0].append(nextBlock)
                if nextBlock not in touchingBlocks: touchingBlocks[nextBlock] = ([],[])
                touchingBlocks[nextBlock][1].append(block)

    removalBlocks = []
    for key in touchingBlocks:
        if not touchingBlocks[key][0] and key not in removalBlocks: removalBlocks.append(key)
        else:
            for aboveBlock in touchingBlocks[key][0]:
                if len([belowBlock for belowBlock in touchingBlocks[aboveBlock][1]]) > 1:
                    # if above block only has more than 1 below bock, add block to removal blocks
                    if key not in removalBlocks: removalBlocks.append(key)

    if USE_LOGGING:
        [print(f'{b}') for b in removalBlocks]
    return len(removalBlocks)

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

solution = getSafeBlocks(input) # 633 to high

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)