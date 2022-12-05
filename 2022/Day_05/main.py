import time
import os

useLogging = True

stackList = []

def getMoveTuple(input):
    words = input.split(" ")
    return [int(words[1]),int(words[3]),int(words[5])]

def getInput(fileName):
    file = open(fileName, 'r')
    input = file.read().split("\n\n")

    moveList = [getMoveTuple(x) for x in input[1].split("\n")]
    startingState = input[0].split("\n")
    stackCount = startingState.pop().strip()

    for i in range(int(stackCount.split(" ").pop())): stackList.append(list()) #initialize empty stacks

    for line in startingState:
        if useLogging: print(line)
        for i in range((len(line)+1)//4):
            if line[i*4] == "[": stackList[i].insert(0, line[(i*4)+1])

    if useLogging: 
        print(stackList)
        print(moveList)

    return moveList

def crateMover9000(instructions):

    for instruction in instructions:
        numCrates = instruction[0]
        sourceStack = instruction[1]-1
        destinationStack = instruction[2]-1

        for move in range(numCrates):
            stackList[destinationStack].append(stackList[sourceStack].pop())

def crateMover9001(instructions):

    for instruction in instructions:
        numCrates = instruction[0]
        sourceStack = instruction[1]-1
        destinationStack = instruction[2]-1

        destinationLength = len(stackList[destinationStack])

        for move in range(numCrates):
            stackList[destinationStack].insert(destinationLength, stackList[sourceStack].pop())

#start of main
useDemo = False
partOne = False
solution = ""

startTime = time.time()

file = 'example.txt' if useDemo else 'input1.txt'
moveList = getInput(file)

crateMover9000(moveList) if partOne else crateMover9001(moveList)

for stack in stackList:
    solution += stack[-1]

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)