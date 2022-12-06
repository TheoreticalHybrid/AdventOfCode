import time
import os

useLogging = True

def getInput(fileName):
    file = open(fileName, 'r')
    input = file.readlines()

    if useLogging: 
        print(input)

    return input

def getStartOfPacketMarker(input, charCount):
    marker = ""
    i = 1
    
    for char in input:
        marker += char

        if i >= charCount:
            if not any(marker.count(c) > 1 for c in marker): return i
            marker = marker[1:]

        i += 1

#start of main
useDemo = False
partOne = False
solution = ""

startTime = time.time()

file = 'example.txt' if useDemo else 'input1.txt'
input = getInput(file)

for line in input:
    print(f'S Packet Index: ', getStartOfPacketMarker(line, 4))
    print(f'E Packet Index: ', getStartOfPacketMarker(line, 14))   
    print()

endtime = time.time()
print ('Completion time: ', endtime - startTime)